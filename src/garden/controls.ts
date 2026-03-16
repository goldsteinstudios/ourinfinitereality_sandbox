import * as THREE from 'three';
import type { Simulation, SimState, ExposureMode } from './simulation';
import type { GardenScene } from './scene';
import { GARDEN_SIZE } from './sand';

export function createControls(
  simulation: Simulation,
  gardenScene: GardenScene,
  container: HTMLElement
): { dispose: () => void } {
  // --- UI overlay ---
  const ui = document.createElement('div');
  ui.className = 'garden-ui';
  ui.innerHTML = `
    <div class="garden-panel garden-top-bar">
      <span class="garden-day-counter">Day 0</span>
      <span class="garden-phase">Ready</span>
    </div>
    <div class="garden-panel garden-controls">
      <button class="garden-btn" data-action="next-day">Next Day</button>
      <button class="garden-btn garden-btn-secondary" data-action="clear-rake">Clear Rake</button>
      <button class="garden-btn garden-btn-secondary" data-action="reset">Reset</button>
    </div>
    <div class="garden-panel garden-settings">
      <div class="garden-setting-row">
        <label>Mode</label>
        <select data-setting="exposure-mode">
          <option value="multi-day">Multi-day</option>
          <option value="single-night">Single night</option>
        </select>
      </div>
      <div class="garden-setting-row">
        <label>Debris</label>
        <input type="range" data-setting="debris-count" min="3" max="20" value="8" />
        <span class="garden-debris-value">8</span>
      </div>
      <div class="garden-setting-row garden-maxdays-row">
        <label>Max days</label>
        <input type="range" data-setting="max-days" min="3" max="14" value="7" />
        <span class="garden-maxdays-value">7</span>
      </div>
      <div class="garden-setting-row">
        <label>Direction</label>
        <select data-setting="rake-direction">
          <option value="horizontal">Horizontal</option>
          <option value="vertical">Vertical</option>
          <option value="diagonal-r">Diagonal &#x2198;</option>
          <option value="diagonal-l">Diagonal &#x2199;</option>
        </select>
      </div>
      <div class="garden-setting-row">
        <label>Animate</label>
        <input type="checkbox" data-setting="animate-rake" checked />
      </div>
      <div class="garden-setting-divider"></div>
      <div class="garden-setting-row">
        <label>Spacing</label>
        <input type="range" data-setting="line-spacing" min="0.2" max="1.0" step="0.05" value="0.4" />
        <span class="garden-spacing-value">0.4</span>
      </div>
      <div class="garden-setting-row">
        <label>Detail</label>
        <input type="range" data-setting="step-size" min="0.05" max="0.2" step="0.01" value="0.12" />
        <span class="garden-stepsize-value">0.12</span>
      </div>
      <div class="garden-setting-row">
        <label>Tightness</label>
        <input type="range" data-setting="correction" min="0.05" max="0.3" step="0.01" value="0.15" />
        <span class="garden-correction-value">0.15</span>
      </div>
    </div>
    <div class="garden-panel garden-hint" style="display:none;">
      Click on the sand to start raking
    </div>
    <div class="garden-toast" style="display:none;">
      Already raked here
    </div>
  `;
  container.appendChild(ui);

  // --- Element references ---
  const dayCounter = ui.querySelector('.garden-day-counter') as HTMLElement;
  const phaseDisplay = ui.querySelector('.garden-phase') as HTMLElement;
  const debrisValue = ui.querySelector('.garden-debris-value') as HTMLElement;
  const maxDaysValue = ui.querySelector('.garden-maxdays-value') as HTMLElement;
  const maxDaysRow = ui.querySelector('.garden-maxdays-row') as HTMLElement;
  const hintPanel = ui.querySelector('.garden-hint') as HTMLElement;
  const toastEl = ui.querySelector('.garden-toast') as HTMLElement;

  const btnNextDay = ui.querySelector('[data-action="next-day"]') as HTMLButtonElement;
  const btnClearRake = ui.querySelector('[data-action="clear-rake"]') as HTMLButtonElement;
  const btnReset = ui.querySelector('[data-action="reset"]') as HTMLButtonElement;

  const selectExposure = ui.querySelector('[data-setting="exposure-mode"]') as HTMLSelectElement;
  const sliderDebris = ui.querySelector('[data-setting="debris-count"]') as HTMLInputElement;
  const sliderMaxDays = ui.querySelector('[data-setting="max-days"]') as HTMLInputElement;
  const selectDirection = ui.querySelector('[data-setting="rake-direction"]') as HTMLSelectElement;
  const checkAnimate = ui.querySelector('[data-setting="animate-rake"]') as HTMLInputElement;
  const sliderSpacing = ui.querySelector('[data-setting="line-spacing"]') as HTMLInputElement;
  const sliderStepSize = ui.querySelector('[data-setting="step-size"]') as HTMLInputElement;
  const sliderCorrection = ui.querySelector('[data-setting="correction"]') as HTMLInputElement;
  const spacingValue = ui.querySelector('.garden-spacing-value') as HTMLElement;
  const stepSizeValue = ui.querySelector('.garden-stepsize-value') as HTMLElement;
  const correctionValue = ui.querySelector('.garden-correction-value') as HTMLElement;

  // --- Toast notification ---
  let toastTimeout: number | null = null;

  function showToast(message: string) {
    toastEl.textContent = message;
    toastEl.style.display = 'block';
    toastEl.style.opacity = '1';

    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }

    toastTimeout = window.setTimeout(() => {
      toastEl.style.opacity = '0';
      setTimeout(() => {
        toastEl.style.display = 'none';
      }, 300);
    }, 1500);
  }

  // --- State update ---
  const phaseLabels: Record<string, string> = {
    idle: 'Ready',
    cleanup: 'Cleaning up...',
    'debris-falling': 'Debris falling...',
    'awaiting-rake': 'Awaiting rake',
    'awaiting-start': 'Click to rake',
    raking: 'Raking...',
  };

  function updateUI(state: SimState) {
    dayCounter.textContent = `Day ${state.day}`;
    phaseDisplay.textContent = phaseLabels[state.phase] || state.phase;

    // Disable buttons during transitions
    const isTransitioning = state.phase === 'cleanup' || state.phase === 'debris-falling' || state.phase === 'raking';
    btnNextDay.disabled = isTransitioning;
    btnClearRake.disabled = isTransitioning;

    // Show hint when awaiting start
    hintPanel.style.display = state.phase === 'awaiting-start' ? 'block' : 'none';

    // Show/hide max days setting based on exposure mode
    maxDaysRow.style.display = state.config.exposureMode === 'multi-day' ? '' : 'none';
  }

  simulation.onStateChange(updateUI);

  // --- Button handlers ---
  btnNextDay.addEventListener('click', () => {
    simulation.nextDay();
  });

  btnClearRake.addEventListener('click', () => {
    simulation.rake(); // This now clears and sets to awaiting-start
  });

  btnReset.addEventListener('click', () => {
    simulation.reset();
  });

  // --- Setting handlers ---
  selectExposure.addEventListener('change', () => {
    simulation.setConfig({ exposureMode: selectExposure.value as ExposureMode });
  });

  sliderDebris.addEventListener('input', () => {
    const val = parseInt(sliderDebris.value, 10);
    debrisValue.textContent = String(val);
    simulation.setConfig({ debrisPerDay: val });
  });

  sliderMaxDays.addEventListener('input', () => {
    const val = parseInt(sliderMaxDays.value, 10);
    maxDaysValue.textContent = String(val);
    simulation.setConfig({ maxDays: val });
  });

  checkAnimate.addEventListener('change', () => {
    simulation.setAnimateRake(checkAnimate.checked);
  });

  sliderSpacing.addEventListener('input', () => {
    const val = parseFloat(sliderSpacing.value);
    spacingValue.textContent = val.toFixed(2);
    const state = simulation.getState();
    simulation.setConfig({
      rakeConfig: { ...state.config.rakeConfig, lineSpacing: val }
    });
  });

  sliderStepSize.addEventListener('input', () => {
    const val = parseFloat(sliderStepSize.value);
    stepSizeValue.textContent = val.toFixed(2);
    const state = simulation.getState();
    simulation.setConfig({
      rakeConfig: { ...state.config.rakeConfig, stepSize: val }
    });
  });

  sliderCorrection.addEventListener('input', () => {
    const val = parseFloat(sliderCorrection.value);
    correctionValue.textContent = val.toFixed(2);
    const state = simulation.getState();
    simulation.setConfig({
      rakeConfig: { ...state.config.rakeConfig, correctionStrength: val }
    });
  });

  function getRakeDirection(): THREE.Vector2 {
    switch (selectDirection.value) {
      case 'vertical': return new THREE.Vector2(0, 1);
      case 'diagonal-r': return new THREE.Vector2(0.707, 0.707);
      case 'diagonal-l': return new THREE.Vector2(0.707, -0.707);
      default: return new THREE.Vector2(1, 0);
    }
  }

  // --- Click-to-rake interaction ---
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();

  function getGardenPosition(event: MouseEvent): THREE.Vector3 | null {
    const rect = gardenScene.renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(pointer, gardenScene.camera);
    const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    const intersection = new THREE.Vector3();
    raycaster.ray.intersectPlane(plane, intersection);
    return intersection;
  }

  function isInsideGarden(pos: THREE.Vector3): boolean {
    const halfSize = GARDEN_SIZE / 2 - 0.3;
    return Math.abs(pos.x) < halfSize && Math.abs(pos.z) < halfSize;
  }

  let isDragging = false;
  let dragStart = new THREE.Vector2();

  function onPointerDown(event: MouseEvent) {
    if (event.button !== 0) return; // Left click only

    const state = simulation.getState();

    if (event.shiftKey) {
      // Shift+drag = manual rake direction (legacy behavior)
      const pos = getGardenPosition(event);
      if (pos) {
        isDragging = true;
        dragStart.set(pos.x, pos.z);
        gardenScene.controls.enabled = false;
      }
      return;
    }

    // Normal click - start raking from this point
    if (state.phase === 'awaiting-start') {
      const pos = getGardenPosition(event);
      if (pos && isInsideGarden(pos)) {
        const startPoint = new THREE.Vector2(pos.x, pos.z);
        const dir = getRakeDirection();
        const result = simulation.startRake(startPoint, dir);

        if (result === null) {
          // Already raked here
          showToast('Already raked here');
        }
      }
    }
  }

  function onPointerUp(event: MouseEvent) {
    if (!isDragging) return;
    isDragging = false;
    gardenScene.controls.enabled = true;

    const pos = getGardenPosition(event);
    if (pos) {
      const dir = new THREE.Vector2(pos.x - dragStart.x, pos.z - dragStart.y);
      if (dir.length() > 0.5) {
        dir.normalize();
        // Set the direction selector to match (approximately)
        const angle = Math.atan2(dir.y, dir.x);
        if (Math.abs(angle) < Math.PI / 6) {
          selectDirection.value = 'horizontal';
        } else if (Math.abs(angle - Math.PI / 2) < Math.PI / 6) {
          selectDirection.value = 'vertical';
        } else if (angle > 0) {
          selectDirection.value = 'diagonal-r';
        } else {
          selectDirection.value = 'diagonal-l';
        }
      }
    }
  }

  // Cursor feedback for valid starting points
  function onPointerMove(event: MouseEvent) {
    const state = simulation.getState();
    const canvas = gardenScene.renderer.domElement;

    if (state.phase === 'awaiting-start' && !isDragging) {
      const pos = getGardenPosition(event);
      if (pos && isInsideGarden(pos)) {
        if (state.rakedGrid.isRaked(pos.x, pos.z)) {
          canvas.style.cursor = 'not-allowed';
        } else {
          canvas.style.cursor = 'crosshair';
        }
      } else {
        canvas.style.cursor = 'default';
      }
    } else {
      canvas.style.cursor = 'default';
    }
  }

  const canvas = gardenScene.renderer.domElement;
  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('pointerup', onPointerUp);
  canvas.addEventListener('pointermove', onPointerMove);

  // Initialize UI
  updateUI(simulation.getState());

  function dispose() {
    canvas.removeEventListener('pointerdown', onPointerDown);
    canvas.removeEventListener('pointerup', onPointerUp);
    canvas.removeEventListener('pointermove', onPointerMove);
    if (toastTimeout) {
      clearTimeout(toastTimeout);
    }
    container.removeChild(ui);
  }

  return { dispose };
}
