import * as THREE from 'three';
import { GARDEN_SIZE } from './sand';

// --- Obstacle interface ---

export type ObstacleType = 'leaf' | 'twig' | 'raindrop' | 'footprint' | 'scuff';

export interface Obstacle {
  id: string;
  type: ObstacleType;
  position: THREE.Vector2;
  radius: number;       // radius of influence for flow field
  mesh: THREE.Object3D;
  isHumanTrace: boolean;
  dayCreated: number;
}

// --- Helpers ---

let idCounter = 0;
function nextId(): string {
  return `obs_${idCounter++}`;
}

function randomInGarden(margin: number = 1.5): THREE.Vector2 {
  const half = GARDEN_SIZE / 2 - margin;
  return new THREE.Vector2(
    (Math.random() - 0.5) * 2 * half,
    (Math.random() - 0.5) * 2 * half
  );
}

// --- Natural debris creation ---

function createLeafMesh(): THREE.Mesh {
  const geometry = new THREE.CircleGeometry(0.25, 8);
  geometry.scale(1, 0.6, 1);
  const hue = 0.08 + Math.random() * 0.12; // range of green-brown
  const saturation = 0.3 + Math.random() * 0.4;
  const lightness = 0.25 + Math.random() * 0.2;
  const color = new THREE.Color().setHSL(hue, saturation, lightness);
  const material = new THREE.MeshStandardMaterial({
    color,
    roughness: 0.8,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.rotation.z = Math.random() * Math.PI * 2;
  mesh.position.y = 0.02;
  mesh.castShadow = true;
  return mesh;
}

function createTwigMesh(): THREE.Mesh {
  const length = 0.3 + Math.random() * 0.4;
  const geometry = new THREE.CylinderGeometry(0.02, 0.015, length, 4);
  const material = new THREE.MeshStandardMaterial({
    color: 0x5c4033,
    roughness: 0.9,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.rotation.z = Math.random() * Math.PI;
  mesh.position.y = 0.03;
  mesh.castShadow = true;
  return mesh;
}

function createRaindropMesh(): THREE.Mesh {
  const geometry = new THREE.CircleGeometry(0.12, 12);
  const material = new THREE.MeshStandardMaterial({
    color: 0x9e9580,
    roughness: 0.95,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = 0.005;
  return mesh;
}

// --- Human trace creation ---

function createFootprintMesh(): THREE.Mesh {
  const geometry = new THREE.CircleGeometry(0.18, 8);
  geometry.scale(1, 1.6, 1); // oval
  const material = new THREE.MeshStandardMaterial({
    color: 0xbfb08a,
    roughness: 1.0,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.5,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = 0.003;
  return mesh;
}

function createScuffMesh(): THREE.Mesh {
  const geometry = new THREE.CircleGeometry(0.1 + Math.random() * 0.08, 5);
  const material = new THREE.MeshStandardMaterial({
    color: 0xb5a68a,
    roughness: 1.0,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.4,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.rotation.z = Math.random() * Math.PI * 2;
  mesh.position.y = 0.003;
  return mesh;
}

// --- Debris spawning ---

const debrisCreators: Record<string, () => THREE.Mesh> = {
  leaf: createLeafMesh,
  twig: createTwigMesh,
  raindrop: createRaindropMesh,
};

const debrisRadii: Record<string, number> = {
  leaf: 0.6,
  twig: 0.5,
  raindrop: 0.3,
  footprint: 0.25,
  scuff: 0.15,
};

export function spawnDebris(
  scene: THREE.Scene,
  count: number,
  day: number,
  types: ObstacleType[] = ['leaf', 'twig', 'raindrop']
): Obstacle[] {
  const obstacles: Obstacle[] = [];

  for (let i = 0; i < count; i++) {
    const type = types[Math.floor(Math.random() * types.length)];
    const creator = debrisCreators[type];
    if (!creator) continue;

    const mesh = creator();
    const pos = randomInGarden();
    mesh.position.x = pos.x;
    mesh.position.z = pos.y;
    scene.add(mesh);

    obstacles.push({
      id: nextId(),
      type,
      position: pos,
      radius: debrisRadii[type],
      mesh,
      isHumanTrace: false,
      dayCreated: day,
    });
  }

  return obstacles;
}

// --- Cleanup trace generation ---

export function generateCleanupTraces(
  scene: THREE.Scene,
  debrisToRemove: Obstacle[],
  day: number
): Obstacle[] {
  const traces: Obstacle[] = [];
  if (debrisToRemove.length === 0) return traces;

  // Entry point: edge of the garden
  const entryX = -GARDEN_SIZE / 2 + 1;
  const entryZ = 0;

  debrisToRemove.forEach((debris) => {
    // Generate footprints along path from entry (or previous debris) to this debris
    const startX = traces.length > 0
      ? traces[traces.length - 1].position.x
      : entryX;
    const startZ = traces.length > 0
      ? traces[traces.length - 1].position.y
      : entryZ;

    const dx = debris.position.x - startX;
    const dz = debris.position.y - startZ;
    const dist = Math.sqrt(dx * dx + dz * dz);
    const stepSize = 0.7;
    const steps = Math.max(2, Math.floor(dist / stepSize));

    for (let s = 1; s <= steps; s++) {
      const t = s / (steps + 1);
      const fx = startX + dx * t + (Math.random() - 0.5) * 0.15;
      const fz = startZ + dz * t + (Math.random() - 0.5) * 0.15;
      const pos = new THREE.Vector2(fx, fz);

      // Check within garden bounds
      const half = GARDEN_SIZE / 2 - 0.5;
      if (Math.abs(pos.x) > half || Math.abs(pos.y) > half) continue;

      const mesh = createFootprintMesh();
      // Orient footprint along walking direction
      mesh.rotation.z = Math.atan2(dz, dx);
      mesh.position.x = pos.x;
      mesh.position.z = pos.y;
      scene.add(mesh);

      traces.push({
        id: nextId(),
        type: 'footprint',
        position: pos,
        radius: debrisRadii.footprint,
        mesh,
        isHumanTrace: true,
        dayCreated: day,
      });
    }

    // Scuff mark near where debris was picked up
    const scuffCount = 1 + Math.floor(Math.random() * 2);
    for (let s = 0; s < scuffCount; s++) {
      const sx = debris.position.x + (Math.random() - 0.5) * 0.4;
      const sz = debris.position.y + (Math.random() - 0.5) * 0.4;
      const pos = new THREE.Vector2(sx, sz);

      const mesh = createScuffMesh();
      mesh.position.x = pos.x;
      mesh.position.z = pos.y;
      scene.add(mesh);

      traces.push({
        id: nextId(),
        type: 'scuff',
        position: pos,
        radius: debrisRadii.scuff,
        mesh,
        isHumanTrace: true,
        dayCreated: day,
      });
    }
  });

  return traces;
}

export function removeObstacles(scene: THREE.Scene, obstacles: Obstacle[]): void {
  obstacles.forEach((obs) => {
    scene.remove(obs.mesh);
    if (obs.mesh instanceof THREE.Mesh) {
      obs.mesh.geometry.dispose();
      (obs.mesh.material as THREE.Material).dispose();
    }
  });
}
