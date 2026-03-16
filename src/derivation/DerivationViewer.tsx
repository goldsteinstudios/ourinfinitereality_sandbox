import { useState, useRef, useEffect, useMemo } from 'react';
import { StepCard } from './StepCard';
import { GeometricCanvas } from './GeometricCanvas';
import {
  DERIVATION_STEPS,
  STRUCTURAL_ELEMENTS,
  THREE_EQUATIONS,
  FALSIFIABLE_PREDICTIONS,
} from '../../data/derivationChain';
import type { GeometricFeature } from '../../types/rsm';

export function DerivationViewer() {
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [showPredictions, setShowPredictions] = useState(false);
  const stepListRef = useRef<HTMLDivElement>(null);

  const activeStep = DERIVATION_STEPS[activeStepIndex];

  // Collect all geometric features visible up to active step
  const visibleFeatures = useMemo<GeometricFeature[]>(() => {
    const features: GeometricFeature[] = [];
    for (let i = 0; i <= activeStepIndex; i++) {
      const step = DERIVATION_STEPS[i];
      if (step.geometricFeature) {
        features.push(step.geometricFeature);
      }
    }
    return features;
  }, [activeStepIndex]);

  // Scroll active step into view
  useEffect(() => {
    const container = stepListRef.current;
    if (!container) return;
    const activeCard = container.children[activeStepIndex] as HTMLElement | undefined;
    if (activeCard) {
      activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [activeStepIndex]);

  const goToPrev = () => {
    if (activeStepIndex > 0) setActiveStepIndex(activeStepIndex - 1);
  };

  const goToNext = () => {
    if (activeStepIndex < DERIVATION_STEPS.length - 1)
      setActiveStepIndex(activeStepIndex + 1);
  };

  return (
    <div className="flex h-full overflow-hidden">
      {/* Left column: Step walkthrough (60%) */}
      <div className="w-3/5 flex flex-col border-r border-gray-700">
        {/* Header */}
        <div className="p-4 border-b border-gray-700 bg-gray-800/50">
          <h2 className="text-lg font-bold text-white">
            RSM v5.5 Derivation Chain
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            14-step entailment chain — each step IS the next (identity, not
            production)
          </p>
          {/* Progress indicator */}
          <div className="flex gap-1 mt-3">
            {DERIVATION_STEPS.map((step, i) => (
              <button
                key={step.id}
                onClick={() => setActiveStepIndex(i)}
                className={`h-1.5 flex-1 rounded-full transition-colors ${
                  i <= activeStepIndex ? 'bg-blue-500' : 'bg-gray-700'
                }`}
                title={step.section}
              />
            ))}
          </div>
        </div>

        {/* Step list */}
        <div
          ref={stepListRef}
          className="flex-1 overflow-y-auto p-4 space-y-0"
        >
          {DERIVATION_STEPS.map((step, index) => (
            <StepCard
              key={step.id}
              step={step}
              isActive={index === activeStepIndex}
              onClick={() => setActiveStepIndex(index)}
              isLast={index === DERIVATION_STEPS.length - 1}
            />
          ))}
        </div>

        {/* Navigation */}
        <div className="p-3 border-t border-gray-700 flex items-center justify-between bg-gray-800/50">
          <button
            onClick={goToPrev}
            disabled={activeStepIndex === 0}
            className="px-4 py-2 rounded text-sm font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-gray-700 hover:bg-gray-600 text-white"
          >
            ← Previous
          </button>
          <span className="text-xs text-gray-400">
            Step {activeStepIndex + 1} of {DERIVATION_STEPS.length}
          </span>
          <button
            onClick={goToNext}
            disabled={activeStepIndex === DERIVATION_STEPS.length - 1}
            className="px-4 py-2 rounded text-sm font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-blue-600 hover:bg-blue-500 text-white"
          >
            Next →
          </button>
        </div>
      </div>

      {/* Right column: Canvas + reference (40%) */}
      <div className="w-2/5 flex flex-col overflow-y-auto">
        {/* Geometric canvas */}
        <div className="p-4 flex-shrink-0" style={{ height: '50%', minHeight: 320 }}>
          <h3 className="text-sm font-semibold text-gray-300 mb-2">
            Geometric Visualization
          </h3>
          <div className="h-[calc(100%-24px)]">
            <GeometricCanvas
              activeStepId={activeStep.id}
              features={visibleFeatures}
            />
          </div>
        </div>

        {/* Three Equations */}
        <div className="px-4 pb-3 flex-shrink-0">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">
            Three Equations
          </h3>
          <div className="grid grid-cols-3 gap-2">
            <div className="bg-gray-800 rounded p-2 text-center">
              <div className="font-mono text-blue-300 text-sm">
                {THREE_EQUATIONS.flat}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                flat constraint
              </div>
            </div>
            <div className="bg-gray-800 rounded p-2 text-center">
              <div className="font-mono text-purple-300 text-sm">
                {THREE_EQUATIONS.circle}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                circular bridge
              </div>
            </div>
            <div className="bg-gray-800 rounded p-2 text-center">
              <div className="font-mono text-emerald-300 text-sm">
                {THREE_EQUATIONS.sphere}
              </div>
              <div className="text-[10px] text-gray-500 mt-1">
                spherical isotropy
              </div>
            </div>
          </div>
        </div>

        {/* Notation reference */}
        <div className="px-4 pb-3 flex-shrink-0">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">
            Structural Elements
          </h3>
          <div className="bg-gray-800 rounded overflow-hidden">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="px-2 py-1.5 text-left text-gray-400 font-medium">
                    Symbol
                  </th>
                  <th className="px-2 py-1.5 text-left text-gray-400 font-medium">
                    Name
                  </th>
                  <th className="px-2 py-1.5 text-left text-gray-400 font-medium">
                    Role
                  </th>
                </tr>
              </thead>
              <tbody>
                {STRUCTURAL_ELEMENTS.map((el) => (
                  <tr
                    key={el.symbol}
                    className="border-b border-gray-700/50 hover:bg-gray-700/30"
                  >
                    <td className="px-2 py-1.5 font-mono text-blue-300">
                      {el.symbol}
                    </td>
                    <td className="px-2 py-1.5 text-gray-200">{el.name}</td>
                    <td className="px-2 py-1.5 text-gray-400">{el.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Falsifiable Predictions (collapsible) */}
        <div className="px-4 pb-4 flex-shrink-0">
          <button
            onClick={() => setShowPredictions(!showPredictions)}
            className="text-sm font-semibold text-gray-300 mb-2 hover:text-white transition-colors flex items-center gap-1"
          >
            <span>{showPredictions ? '▾' : '▸'}</span>
            Falsifiable Predictions ({FALSIFIABLE_PREDICTIONS.length})
          </button>
          {showPredictions && (
            <div className="space-y-2">
              {FALSIFIABLE_PREDICTIONS.map((pred) => (
                <div
                  key={pred.id}
                  className="bg-gray-800 rounded p-2 text-xs"
                >
                  <div className="text-gray-200 mb-1">
                    <span className="text-blue-400 font-mono mr-1">
                      #{pred.id}
                    </span>
                    {pred.claim}
                  </div>
                  <div className="text-gray-500">
                    <span className="text-red-400 font-medium">
                      Falsified by:
                    </span>{' '}
                    {pred.falsifier}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
