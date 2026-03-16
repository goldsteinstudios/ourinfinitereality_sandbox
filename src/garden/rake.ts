import * as THREE from 'three';
import type { Obstacle } from './debris';
import { GARDEN_SIZE } from './sand';

// Interface for raked area checking (avoids circular import with simulation.ts)
export interface RakedAreaChecker {
  isRaked(x: number, z: number): boolean;
}

// --- Rake Configuration ---

export interface RakeConfig {
  lineSpacing: number;      // Distance between lines (0.2 - 1.0)
  stepSize: number;         // Path resolution (0.05 - 0.2)
  correctionStrength: number; // How tightly to follow contours (0.05 - 0.3)
}

export const DEFAULT_RAKE_CONFIG: RakeConfig = {
  lineSpacing: 0.4,
  stepSize: 0.12,
  correctionStrength: 0.15,
};

// --- Walking Path Result ---

export interface WalkResult {
  path: THREE.Vector3[];
  stoppedReason: 'edge' | 'obstacle' | 'crossed' | 'stuck';
}

// --- Constants ---

const MAX_STEPS = 5000;
const OBSTACLE_MARGIN = 0.25;

// --- Helper functions ---

function isInBounds(x: number, z: number, margin: number = 0.3): boolean {
  const halfSize = GARDEN_SIZE / 2 - margin;
  return Math.abs(x) < halfSize && Math.abs(z) < halfSize;
}

function isBlockedByObstacle(x: number, z: number, obstacles: Obstacle[]): boolean {
  for (const obs of obstacles) {
    const dx = x - obs.position.x;
    const dz = z - obs.position.y;
    const dist = Math.sqrt(dx * dx + dz * dz);
    if (dist < obs.radius + OBSTACLE_MARGIN) {
      return true;
    }
  }
  return false;
}

function isBlocked(
  x: number,
  z: number,
  obstacles: Obstacle[],
  rakedGrid: RakedAreaChecker
): boolean {
  if (!isInBounds(x, z)) return true;
  if (isBlockedByObstacle(x, z, obstacles)) return true;
  if (rakedGrid.isRaked(x, z)) return true;
  return false;
}

// Rotate direction 90 degrees left (counterclockwise)
function turnLeft(dir: THREE.Vector2): THREE.Vector2 {
  return new THREE.Vector2(-dir.y, dir.x);
}

// Rotate direction 90 degrees right (clockwise)
function turnRight(dir: THREE.Vector2): THREE.Vector2 {
  return new THREE.Vector2(dir.y, -dir.x);
}

// --- Main Walking Path Algorithm ---
// Contour following: maintain fixed distance from nearest wall, move tangentially

export function computeWalkingPath(
  start: THREE.Vector2,
  obstacles: Obstacle[],
  rakedGrid: RakedAreaChecker,
  direction: THREE.Vector2 = new THREE.Vector2(1, 0),
  config: RakeConfig = DEFAULT_RAKE_CONFIG
): WalkResult {
  const path: THREE.Vector3[] = [];
  let stoppedReason: WalkResult['stoppedReason'] = 'stuck';

  const TARGET_DISTANCE = config.lineSpacing;
  const STEP_SIZE = config.stepSize;
  const CORRECTION_STRENGTH = config.correctionStrength;
  const LOOKBACK_SKIP = Math.max(20, Math.floor(TARGET_DISTANCE / STEP_SIZE) * 2);

  let x = start.x;
  let z = start.y;
  let stuckCount = 0;

  // Current direction - starts as the initial direction, updated when following contours
  let dirX = direction.x;
  let dirZ = direction.y;
  const dirLen = Math.sqrt(dirX * dirX + dirZ * dirZ);
  dirX /= dirLen;
  dirZ /= dirLen;

  // Find nearest point and distance to own path (excluding recent points)
  function nearestOnOwnPath(px: number, pz: number): { dist: number; nx: number; nz: number } {
    let minDist = Infinity;
    let nearestX = px;
    let nearestZ = pz;
    const checkEnd = Math.max(0, path.length - LOOKBACK_SKIP);
    for (let i = 0; i < checkEnd; i++) {
      const pt = path[i];
      const dx = px - pt.x;
      const dz = pz - pt.z;
      const dist = Math.sqrt(dx * dx + dz * dz);
      if (dist < minDist) {
        minDist = dist;
        nearestX = pt.x;
        nearestZ = pt.z;
      }
    }
    return { dist: minDist, nx: nearestX, nz: nearestZ };
  }

  // Find nearest point and distance to obstacles
  function nearestOnObstacles(px: number, pz: number): { dist: number; nx: number; nz: number } {
    let minDist = Infinity;
    let nearestX = px;
    let nearestZ = pz;
    for (const obs of obstacles) {
      const dx = px - obs.position.x;
      const dz = pz - obs.position.y;
      const d = Math.sqrt(dx * dx + dz * dz);
      const dist = d - obs.radius;
      if (dist < minDist) {
        minDist = dist;
        // Nearest point on obstacle surface
        nearestX = obs.position.x + (dx / d) * obs.radius;
        nearestZ = obs.position.y + (dz / d) * obs.radius;
      }
    }
    return { dist: minDist, nx: nearestX, nz: nearestZ };
  }

  // Find nearest point and distance to edge
  function nearestOnEdge(px: number, pz: number): { dist: number; nx: number; nz: number } {
    const halfSize = GARDEN_SIZE / 2;
    const distLeft = px + halfSize;
    const distRight = halfSize - px;
    const distBottom = pz + halfSize;
    const distTop = halfSize - pz;

    const minDist = Math.min(distLeft, distRight, distBottom, distTop);
    let nearestX = px;
    let nearestZ = pz;

    if (minDist === distLeft) { nearestX = -halfSize; nearestZ = pz; }
    else if (minDist === distRight) { nearestX = halfSize; nearestZ = pz; }
    else if (minDist === distBottom) { nearestX = px; nearestZ = -halfSize; }
    else { nearestX = px; nearestZ = halfSize; }

    return { dist: minDist, nx: nearestX, nz: nearestZ };
  }

  // Find the nearest wall point (edge, obstacle, or own path)
  function nearestWall(px: number, pz: number): { dist: number; nx: number; nz: number } {
    const edge = nearestOnEdge(px, pz);
    const obs = nearestOnObstacles(px, pz);
    const own = nearestOnOwnPath(px, pz);

    // Also check previously raked areas
    let rakedDist = Infinity;
    let rakedX = px, rakedZ = pz;
    for (let angle = 0; angle < Math.PI * 2; angle += 0.2) {
      for (let r = 0.1; r < 3; r += 0.1) {
        const cx = px + Math.cos(angle) * r;
        const cz = pz + Math.sin(angle) * r;
        if (rakedGrid.isRaked(cx, cz)) {
          if (r < rakedDist) {
            rakedDist = r;
            rakedX = cx;
            rakedZ = cz;
          }
          break;
        }
      }
    }

    // Return the nearest one
    let nearest = edge;
    if (obs.dist < nearest.dist) nearest = obs;
    if (own.dist < nearest.dist) nearest = own;
    if (rakedDist < nearest.dist) nearest = { dist: rakedDist, nx: rakedX, nz: rakedZ };

    return nearest;
  }

  // Check if a point is blocked (too close to wall)
  function isBlocked(px: number, pz: number): boolean {
    const wall = nearestWall(px, pz);
    return wall.dist < TARGET_DISTANCE * 0.3;
  }

  for (let step = 0; step < MAX_STEPS; step++) {
    path.push(new THREE.Vector3(x, 0, z));

    // Find nearest wall
    const wall = nearestWall(x, z);

    if (wall.dist < Infinity && wall.dist < TARGET_DISTANCE * 2) {
      // Close to a wall - follow the contour
      // Direction away from wall (outward normal)
      const awayX = x - wall.nx;
      const awayZ = z - wall.nz;
      const awayLen = Math.sqrt(awayX * awayX + awayZ * awayZ);

      if (awayLen > 0.001) {
        const normX = awayX / awayLen;
        const normZ = awayZ / awayLen;

        // Tangent direction (perpendicular to normal, going "left" / counterclockwise)
        const tangentX = -normZ;
        const tangentZ = normX;

        // Update our direction to follow the contour
        dirX = tangentX;
        dirZ = tangentZ;

        // Distance error
        const error = wall.dist - TARGET_DISTANCE;

        // Move in tangent direction, with correction toward/away from wall
        const moveX = tangentX * STEP_SIZE + normX * error * CORRECTION_STRENGTH;
        const moveZ = tangentZ * STEP_SIZE + normZ * error * CORRECTION_STRENGTH;

        const nextX = x + moveX;
        const nextZ = z + moveZ;

        if (!isBlocked(nextX, nextZ)) {
          x = nextX;
          z = nextZ;
          stuckCount = 0;
        } else {
          stuckCount++;
          // Try moving just along tangent
          const altX = x + tangentX * STEP_SIZE * 0.5;
          const altZ = z + tangentZ * STEP_SIZE * 0.5;
          if (!isBlocked(altX, altZ)) {
            x = altX;
            z = altZ;
          }
        }
      } else {
        stuckCount++;
      }
    } else {
      // No wall nearby - go straight in current direction until we hit something
      const nextX = x + dirX * STEP_SIZE;
      const nextZ = z + dirZ * STEP_SIZE;

      if (!isBlocked(nextX, nextZ)) {
        x = nextX;
        z = nextZ;
        stuckCount = 0;
      } else {
        // Hit something while going straight - we'll start following it next iteration
        stuckCount++;
      }
    }

    // Check if truly stuck
    if (stuckCount > 50) {
      stoppedReason = 'stuck';
      break;
    }

    // Check if we've looped back to start (completed a full contour)
    if (path.length > 100) {
      const startPt = path[0];
      const dx = x - startPt.x;
      const dz = z - startPt.z;
      if (dx * dx + dz * dz < TARGET_DISTANCE * TARGET_DISTANCE * 0.5) {
        // Completed a loop - this contour is done
        stoppedReason = 'crossed';
        break;
      }
    }
  }

  return { path, stoppedReason };
}

// --- Legacy API (kept for compatibility) ---

export interface RakeResult {
  lines: THREE.Vector3[][];
}

export function computeRakeLines(
  obstacles: Obstacle[],
  direction: THREE.Vector2 = new THREE.Vector2(1, 0),
  lineSpacing: number = 0.4,
  resolution: number = 100
): RakeResult {
  return { lines: [] };
}
