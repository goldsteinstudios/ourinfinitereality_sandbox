import * as THREE from 'three';

export interface Sand {
  mesh: THREE.Mesh;
  rakeGroup: THREE.Group;
  clearRakeLines: () => void;
  addRakeLines: (lines: THREE.Vector3[][]) => void;
  dispose: () => void;
}

const GARDEN_SIZE = 20;

export function createSand(scene: THREE.Scene): Sand {
  // Sand plane
  const geometry = new THREE.PlaneGeometry(GARDEN_SIZE, GARDEN_SIZE, 1, 1);
  const material = new THREE.MeshStandardMaterial({
    color: 0xd4c9a8,
    roughness: 0.9,
    metalness: 0.0,
  });

  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = -Math.PI / 2;
  mesh.receiveShadow = true;
  scene.add(mesh);

  // Border frame (wooden edge)
  const borderMaterial = new THREE.MeshStandardMaterial({
    color: 0x5c4033,
    roughness: 0.7,
  });
  const borderThickness = 0.3;
  const borderHeight = 0.15;
  const halfSize = GARDEN_SIZE / 2;

  const borders = [
    { pos: [0, borderHeight / 2, -halfSize], scale: [GARDEN_SIZE + borderThickness * 2, borderHeight, borderThickness] },
    { pos: [0, borderHeight / 2, halfSize], scale: [GARDEN_SIZE + borderThickness * 2, borderHeight, borderThickness] },
    { pos: [-halfSize, borderHeight / 2, 0], scale: [borderThickness, borderHeight, GARDEN_SIZE] },
    { pos: [halfSize, borderHeight / 2, 0], scale: [borderThickness, borderHeight, GARDEN_SIZE] },
  ];

  const borderGeom = new THREE.BoxGeometry(1, 1, 1);
  borders.forEach(({ pos, scale }) => {
    const border = new THREE.Mesh(borderGeom, borderMaterial);
    border.position.set(pos[0], pos[1], pos[2]);
    border.scale.set(scale[0], scale[1], scale[2]);
    border.castShadow = true;
    border.receiveShadow = true;
    scene.add(border);
  });

  // Rake lines group
  const rakeGroup = new THREE.Group();
  rakeGroup.position.y = 0.01; // Sit just above the sand surface
  scene.add(rakeGroup);

  function clearRakeLines() {
    while (rakeGroup.children.length > 0) {
      const child = rakeGroup.children[0];
      rakeGroup.remove(child);
      if (child instanceof THREE.Line) {
        child.geometry.dispose();
        (child.material as THREE.Material).dispose();
      }
    }
  }

  function addRakeLines(lines: THREE.Vector3[][]) {
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0xbfb08a,
      linewidth: 1,
    });
    const shadowMaterial = new THREE.LineBasicMaterial({
      color: 0xc8bc9e,
      linewidth: 1,
    });

    lines.forEach((points) => {
      if (points.length < 2) return;

      // Create smooth curve from points
      const curve = new THREE.CatmullRomCurve3(points);
      const curvePoints = curve.getPoints(points.length * 3);

      // Main groove line (slightly darker)
      const geometry = new THREE.BufferGeometry().setFromPoints(curvePoints);
      const line = new THREE.Line(geometry, lineMaterial.clone());
      rakeGroup.add(line);

      // Highlight line (slightly offset, lighter — gives 3D groove illusion)
      const offsetPoints = curvePoints.map(
        (p) => new THREE.Vector3(p.x + 0.02, p.y + 0.005, p.z + 0.02)
      );
      const shadowGeometry = new THREE.BufferGeometry().setFromPoints(offsetPoints);
      const shadowLine = new THREE.Line(shadowGeometry, shadowMaterial.clone());
      rakeGroup.add(shadowLine);
    });
  }

  function dispose() {
    clearRakeLines();
    geometry.dispose();
    material.dispose();
    borderGeom.dispose();
    borderMaterial.dispose();
    scene.remove(mesh);
    scene.remove(rakeGroup);
  }

  return { mesh, rakeGroup, clearRakeLines, addRakeLines, dispose };
}

export { GARDEN_SIZE };
