import { useState } from 'react';
import type { DerivationStep } from '../../types/rsm';

interface StepCardProps {
  step: DerivationStep;
  isActive: boolean;
  onClick: () => void;
  isLast: boolean;
}

export function StepCard({ step, isActive, onClick, isLast }: StepCardProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="relative">
      {/* Step card */}
      <button
        onClick={onClick}
        className={`w-full text-left rounded-lg border transition-all duration-200 ${
          isActive
            ? 'bg-gray-700 border-blue-500 shadow-lg shadow-blue-500/10'
            : 'bg-gray-800 border-gray-700 hover:border-gray-600 hover:bg-gray-750'
        }`}
      >
        <div className="p-4">
          {/* Section badge + title */}
          <div className="flex items-start gap-3 mb-2">
            <span
              className={`inline-flex items-center justify-center px-2 py-0.5 rounded text-xs font-mono font-bold shrink-0 ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300'
              }`}
            >
              {step.section}
            </span>
            <h3
              className={`font-semibold text-sm leading-tight ${
                isActive ? 'text-white' : 'text-gray-200'
              }`}
            >
              {step.title}
            </h3>
          </div>

          {/* Core statement (always visible) */}
          <p className="text-sm text-gray-300 leading-relaxed ml-0">
            {step.statement}
          </p>

          {/* Key insight callout */}
          {step.keyInsight && isActive && (
            <div className="mt-3 p-2 bg-blue-900/30 border border-blue-800/50 rounded text-xs text-blue-200 leading-relaxed">
              <span className="font-bold">Key insight:</span> {step.keyInsight}
            </div>
          )}

          {/* Formal notation */}
          {step.notation && isActive && (
            <div className="mt-2 p-2 bg-gray-900 rounded font-mono text-xs text-green-300">
              {step.notation}
            </div>
          )}

          {/* Expand toggle for full explanation */}
          {isActive && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(!expanded);
              }}
              className="mt-3 text-xs text-blue-400 hover:text-blue-300 transition-colors"
            >
              {expanded ? '▾ Hide full explanation' : '▸ Show full explanation'}
            </button>
          )}

          {/* Full explanation (expandable) */}
          {isActive && expanded && (
            <p className="mt-2 text-xs text-gray-400 leading-relaxed">
              {step.explanation}
            </p>
          )}
        </div>
      </button>

      {/* ≡ connector to next step */}
      {!isLast && (
        <div className="flex justify-center py-1">
          <span
            className={`text-lg font-bold ${
              isActive ? 'text-blue-400' : 'text-gray-600'
            }`}
          >
            ≡
          </span>
        </div>
      )}
    </div>
  );
}
