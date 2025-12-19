import React, { useState, useEffect } from 'react';
import { useMotionStore } from '../../store/useMotionStore';
import type { GeometricPattern, PatternAnalysis } from '../../types/motion';

const GEOMETRIC_PATTERNS: { value: GeometricPattern; label: string; description: string }[] = [
  { value: 'circle', label: 'Circle', description: 'Closed circular path' },
  { value: 'spiral', label: 'Spiral', description: 'Expanding or contracting circular path' },
  { value: 'arc', label: 'Arc', description: 'Partial circle' },
  { value: 'line', label: 'Line', description: 'Straight linear path' },
  { value: 'wave', label: 'Wave', description: 'Undulating sinusoidal pattern' },
  { value: 'zigzag', label: 'Zigzag', description: 'Angular back-and-forth' },
  { value: 'helix', label: 'Helix', description: '3D spiral path' },
  { value: 'point', label: 'Point', description: 'Concentrated focal point' },
  { value: 'radial', label: 'Radial', description: 'Expanding from center' },
  { value: 'grid', label: 'Grid', description: 'Orthogonal intersection' },
  { value: 'fractal', label: 'Fractal', description: 'Self-similar recursive pattern' },
];

const MATH_RELATIONS = ['phi', 'pi', 'e', 'fibonacci', 'ratio', 'symmetry', 'recursion'] as const;

export const PatternMatcher: React.FC = () => {
  const { currentInsight, updatePattern } = useMotionStore();
  const [pattern, setPattern] = useState<PatternAnalysis>({
    primaryPattern: 'line',
    secondaryPatterns: [],
    mathematicalRelationships: [],
    naturalExamples: [],
    description: '',
  });
  const [newExample, setNewExample] = useState('');

  useEffect(() => {
    if (currentInsight) {
      setPattern(currentInsight.patternAnalysis);
    }
  }, [currentInsight]);

  const handleSave = () => {
    updatePattern(pattern);
  };

  const toggleSecondary = (p: GeometricPattern) => {
    const newSecondary = pattern.secondaryPatterns.includes(p)
      ? pattern.secondaryPatterns.filter((sp) => sp !== p)
      : [...pattern.secondaryPatterns, p];
    setPattern({ ...pattern, secondaryPatterns: newSecondary });
    handleSave();
  };

  const addNaturalExample = () => {
    if (newExample.trim()) {
      setPattern({
        ...pattern,
        naturalExamples: [...pattern.naturalExamples, newExample.trim()],
      });
      setNewExample('');
      handleSave();
    }
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-indigo-900 mb-2">
          <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
          Geometric Pattern
        </h2>
        <p className="text-sm text-indigo-800">
          What geometric pattern does this motion create? Connect it to mathematical relationships
          and natural phenomena.
        </p>
      </div>

      {/* Motion Summary */}
      {currentInsight.physicalAction && (
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <div className="text-sm font-medium text-gray-700 mb-1">Motion Described:</div>
          <div className="text-sm text-gray-600 italic">{currentInsight.physicalAction}</div>
        </div>
      )}

      {/* Primary Pattern */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Primary Geometric Pattern
        </label>
        <div className="grid grid-cols-3 gap-3">
          {GEOMETRIC_PATTERNS.map((p) => (
            <button
              key={p.value}
              onClick={() => {
                setPattern({ ...pattern, primaryPattern: p.value });
                handleSave();
              }}
              className={`p-3 text-left rounded-lg border transition-colors ${
                pattern.primaryPattern === p.value
                  ? 'bg-indigo-100 border-indigo-500'
                  : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
              }`}
            >
              <div className="font-medium text-sm">{p.label}</div>
              <div className="text-xs text-gray-600">{p.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Secondary Patterns */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Secondary Patterns (optional)
        </label>
        <div className="flex flex-wrap gap-2">
          {GEOMETRIC_PATTERNS.filter((p) => p.value !== pattern.primaryPattern).map((p) => (
            <button
              key={p.value}
              onClick={() => toggleSecondary(p.value)}
              className={`px-3 py-2 text-sm rounded-lg transition-colors ${
                pattern.secondaryPatterns.includes(p.value)
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Pattern Description */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Pattern Description
        </label>
        <textarea
          value={pattern.description}
          onChange={(e) => setPattern({ ...pattern, description: e.target.value })}
          onBlur={handleSave}
          placeholder="Describe the geometric pattern this motion creates in space..."
          rows={4}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none"
        />
      </div>

      {/* Natural Examples */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Where does this pattern appear in nature?
        </label>
        <div className="space-y-3">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newExample}
              onChange={(e) => setNewExample(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addNaturalExample()}
              placeholder="e.g., 'tree rings', 'galaxy spirals', 'water ripples'"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            />
            <button
              onClick={addNaturalExample}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {pattern.naturalExamples.map((example, i) => (
              <div
                key={i}
                className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm flex items-center space-x-2"
              >
                <span>{example}</span>
                <button
                  onClick={() => {
                    setPattern({
                      ...pattern,
                      naturalExamples: pattern.naturalExamples.filter((_, idx) => idx !== i),
                    });
                    handleSave();
                  }}
                  className="text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Mathematical Relationships */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Mathematical Relationships (optional)
        </label>
        <div className="text-xs text-gray-500 mb-3">
          Does this pattern relate to φ (golden ratio), π, Fibonacci, or other mathematical
          constants?
        </div>
        <div className="flex flex-wrap gap-2">
          {MATH_RELATIONS.map((rel) => (
            <button
              key={rel}
              className="px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-indigo-100 hover:text-indigo-700 transition-colors"
            >
              {rel}
            </button>
          ))}
        </div>
        <div className="mt-3 text-xs text-gray-500">
          (Full mathematical analysis coming in future update)
        </div>
      </div>

      {/* Example for 利 */}
      {currentInsight.character === '利' && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="text-sm font-medium text-amber-900 mb-2">💡 Example for 利:</div>
          <div className="text-sm text-amber-800 space-y-1">
            <div>
              <strong>Primary:</strong> Spiral (arc motion + forward movement)
            </div>
            <div>
              <strong>Natural Examples:</strong> Growth spirals in plants, spiral cutting patterns,
              golden ratio in shell growth
            </div>
            <div>
              <strong>Math:</strong> φ (golden ratio) - efficient distribution pattern
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
