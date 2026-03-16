import * as THREE from 'three';
import type { Obstacle, ObstacleType } from './debris';
import { spawnDebris, generateCleanupTraces, removeObstacles } from './debris';
import type { Sand } from './sand';
import { GARDEN_SIZE } from './sand';
import { computeWalkingPath, type WalkResult, type RakedAreaChecker, type RakeConfig, DEFAULT_RAKE_CONFIG } from './rake';

// --- Types ---

export type ExposureMode = 'single-night' | 'multi-day';

export type SimPhase =
  | 'idle'
  | 'cleanup'
  | 'debris-falling'
  | 'awaiting-rake'
  | 'awaiting-start'
  | 'raking';

// --- Raked Grid ---

export interface RakedGrid extends RakedAreaChecker {
  resolution: number;
  cells: boolean[][];
  mark(path: THREE.Vector3[]): void;
  clear(): void;
}

function createRakedGrid(resolution: number = 200): RakedGrid {
  const cells: boolean[][] = [];
  const cellSize = GARDEN_SIZE / resolution;
  const halfSize = GARDEN_SIZE / 2;

  // Initialize all cells as unraked
  for (let i = 0; i < resolution; i++) {
    cells[i] = [];
    for (let j = 0; j < resolution; j++) {
      cells[i][j] = false;
    }
  }

  function worldToGrid(x: number, z: number): [number, number] {
    const i = Math.floor((x + halfSize) / cellSize);
    const j = Math.floor((z + halfSize) / cellSize);
    return [
      Math.max(0, Math.min(resolution - 1, i)),
      Math.max(0, Math.min(resolution - 1, j)),
    ];
  }

  function mark(path: THREE.Vector3[]): void {
    // Mark all cells along the path as raked
    // Use Bresenham-style marking with a small brush radius
    const brushRadius = 2; // cells
    for (const point of path) {
      const [ci, cj] = worldToGrid(point.x, point.z);
      for (let di = -brushRadius; di <= brushRadius; di++) {
        for (let dj = -brushRadius; dj <= brushRadius; dj++) {
          const ni = ci + di;
          const nj = cj + dj;
          if (ni >= 0 && ni < resolution && nj >= 0 && nj < resolution) {
            cells[ni][nj] = true;
          }
        }
      }
    }
  }

  function isRaked(x: number, z: number): boolean {
    const [i, j] = worldToGrid(x, z);
    return cells[i][j];
  }

  function clear(): void {
    for (let i = 0; i < resolution; i++) {
      for (let j = 0; j < resolution; j++) {
        cells[i][j] = false;
      }
    }
  }

  return { resolution, cells, mark, isRaked, clear };
}

export interface SimConfig {
  exposureMode: ExposureMode;
  maxDays: number;
  debrisPerDay: number;
  debrisTypes: ObstacleType[];
  rakeConfig: RakeConfig;
}

export interface SimState {
  phase: SimPhase;
  day: number;
  obstacles: Obstacle[];
  config: SimConfig;
  rakedGrid: RakedGrid;
  animateRake: boolean;
}

export interface Simulation {
  getState: () => SimState;
  nextDay: () => void;
  rake: (direction?: THREE.Vector2) => void;
  startRake: (point: THREE.Vector2, direction?: THREE.Vector2) => WalkResult | null;
  reset: () => void;
  setConfig: (partial: Partial<SimConfig>) => void;
  setAnimateRake: (animate: boolean) => void;
  onStateChange: (cb: (state: SimState) => void) => void;
}

// --- Implementation ---

export function createSimulation(
  scene: THREE.Scene,
  sand: Sand
): Simulation {
  const listeners: ((state: SimState) => void)[] = [];

  const state: SimState = {
    phase: 'idle',
    day: 0,
    obstacles: [],
    config: {
      exposureMode: 'multi-day',
      maxDays: 7,
      debrisPerDay: 8,
      debrisTypes: ['leaf', 'twig', 'raindrop'],
      rakeConfig: { ...DEFAULT_RAKE_CONFIG },
    },
    rakedGrid: createRakedGrid(),
    animateRake: true,
  };

  function notify() {
    listeners.forEach((cb) => cb({ ...state }));
  }

  function nextDay() {
    const { config } = state;
    state.day++;

    // --- CLEANUP PHASE ---
    if (config.exposureMode === 'multi-day' && state.obstacles.length > 0) {
      state.phase = 'cleanup';
      notify();

      // Find natural debris to remove (not human traces)
      const naturalDebris = state.obstacles.filter((o) => !o.isHumanTrace);

      // Remove old human traces (older than 1 day)
      const oldTraces = state.obstacles.filter(
        (o) => o.isHumanTrace && o.dayCreated < state.day - 1
      );
      removeObstacles(scene, oldTraces);

      // Generate cleanup traces from current natural debris
      const newTraces = generateCleanupTraces(scene, naturalDebris, state.day);

      // Remove the natural debris
      removeObstacles(scene, naturalDebris);

      // Keep only: surviving human traces + new traces
      const survivingTraces = state.obstacles.filter(
        (o) => o.isHumanTrace && o.dayCreated >= state.day - 1
      );
      state.obstacles = [...survivingTraces, ...newTraces];
    } else if (config.exposureMode === 'single-night') {
      // Wipe everything clean
      state.phase = 'cleanup';
      notify();
      removeObstacles(scene, state.obstacles);
      state.obstacles = [];
    }

    // Clear rake lines and raked grid
    sand.clearRakeLines();
    state.rakedGrid.clear();

    // --- DEBRIS FALLING PHASE ---
    state.phase = 'debris-falling';
    notify();

    const newDebris = spawnDebris(
      scene,
      config.debrisPerDay,
      state.day,
      config.debrisTypes
    );
    state.obstacles = [...state.obstacles, ...newDebris];

    // --- AWAITING START (user clicks to rake) ---
    state.phase = 'awaiting-start';
    notify();

    // Auto-reset check for multi-day mode
    if (
      config.exposureMode === 'multi-day' &&
      state.day >= config.maxDays
    ) {
      // Don't auto-reset — just let the user know max days reached
      // They can manually reset or keep going
    }
  }

  function rake(direction?: THREE.Vector2) {
    // Legacy rake function - now clears and sets to awaiting-start
    state.phase = 'awaiting-start';
    sand.clearRakeLines();
    state.rakedGrid.clear();
    notify();
  }

  function startRake(point: THREE.Vector2, direction?: THREE.Vector2): WalkResult | null {
    // Check if the starting point is already raked
    if (state.rakedGrid.isRaked(point.x, point.y)) {
      return null; // Already raked
    }

    state.phase = 'raking';
    notify();

    const dir = direction || new THREE.Vector2(1, 0);
    const result = computeWalkingPath(
      point,
      state.obstacles,
      state.rakedGrid,
      dir,
      state.config.rakeConfig
    );

    if (result.path.length >= 2) {
      // Mark path as raked
      state.rakedGrid.mark(result.path);

      if (state.animateRake) {
        // Animate path drawing progressively
        animatePathDrawing(result.path);
      } else {
        // Draw instantly
        sand.addRakeLines([result.path]);
      }
    }

    state.phase = 'awaiting-start';
    notify();

    return result;
  }

  function animatePathDrawing(path: THREE.Vector3[]): void {
    const segmentsPerFrame = 5;
    let currentIndex = 0;
    const partialPath: THREE.Vector3[] = [];

    function drawNextSegment() {
      const endIndex = Math.min(currentIndex + segmentsPerFrame, path.length);
      for (let i = currentIndex; i < endIndex; i++) {
        partialPath.push(path[i]);
      }
      currentIndex = endIndex;

      // Redraw the partial path
      // For simplicity, we'll draw the full path once at the end
      // A more sophisticated approach would update incrementally
      if (currentIndex >= path.length) {
        sand.addRakeLines([path]);
      } else {
        requestAnimationFrame(drawNextSegment);
      }
    }

    drawNextSegment();
  }

  function reset() {
    removeObstacles(scene, state.obstacles);
    state.obstacles = [];
    state.day = 0;
    state.phase = 'idle';
    sand.clearRakeLines();
    state.rakedGrid.clear();
    notify();
  }

  function setAnimateRake(animate: boolean) {
    state.animateRake = animate;
  }

  function setConfig(partial: Partial<SimConfig>) {
    Object.assign(state.config, partial);
    notify();
  }

  function onStateChange(cb: (state: SimState) => void) {
    listeners.push(cb);
  }

  return {
    getState: () => ({ ...state }),
    nextDay,
    rake,
    startRake,
    reset,
    setConfig,
    setAnimateRake,
    onStateChange,
  };
}
