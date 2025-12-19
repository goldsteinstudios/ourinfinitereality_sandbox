import React from 'react';
import { useMotionStore } from '../../store/useMotionStore';

export const ReviewPanel: React.FC = () => {
  const { currentInsight, saveInsight, resetDecoder } = useMotionStore();

  const handleSave = () => {
    saveInsight();
    alert(`Motion insight for ${currentInsight?.character} saved successfully!`);
  };

  const handleSaveAndNew = () => {
    saveInsight();
    resetDecoder();
  };

  if (!currentInsight) return null;

  const completionScore = [
    currentInsight.radicals.length > 0,
    currentInsight.tool !== undefined,
    currentInsight.physicalAction.length > 0,
    currentInsight.patternAnalysis.description.length > 0,
    currentInsight.translations.motion.length > 0,
    currentInsight.insights.length > 0 || currentInsight.hypotheses.length > 0,
  ].filter(Boolean).length;

  const completionPercent = Math.round((completionScore / 6) * 100);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-gray-900">
            <span className="text-6xl font-serif mr-4">{currentInsight.character}</span>
            ({currentInsight.pinyin})
          </h2>
          <div className="text-right">
            <div className="text-3xl font-bold text-purple-600">{completionPercent}%</div>
            <div className="text-sm text-gray-600">Complete</div>
          </div>
        </div>
        <p className="text-sm text-gray-700">
          Review your complete motion analysis. Make any final adjustments, then save.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 gap-6">
        {/* Radicals */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">📐 Radicals</h3>
          {currentInsight.radicals.length > 0 ? (
            <div className="space-y-2">
              {currentInsight.radicals.map((r) => (
                <div key={r} className="flex items-center space-x-3">
                  <span className="text-2xl font-serif">{r}</span>
                  <span className="text-sm text-gray-600">
                    {currentInsight.radicalMeanings[r] || '—'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-sm text-gray-500">No radicals identified</div>
          )}
        </div>

        {/* Tool */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">🔧 Tool</h3>
          {currentInsight.tool ? (
            <div className="space-y-1">
              <div className="text-lg font-medium text-gray-800">{currentInsight.tool.name}</div>
              <div className="text-sm text-gray-600">{currentInsight.tool.category}</div>
              <div className="text-sm text-gray-600 mt-2">{currentInsight.tool.description}</div>
            </div>
          ) : (
            <div className="text-sm text-gray-500">No tool / Abstract concept</div>
          )}
        </div>

        {/* Motion */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 col-span-2">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">🎬 Physical Motion</h3>
          {currentInsight.physicalAction ? (
            <div className="space-y-3">
              <div className="text-sm text-gray-700 italic bg-gray-50 p-3 rounded">
                {currentInsight.physicalAction}
              </div>
              <div className="grid grid-cols-4 gap-3 text-sm">
                <div>
                  <div className="font-medium text-gray-700">Direction</div>
                  <div className="text-gray-600">{currentInsight.motionDescription.directionality}</div>
                </div>
                <div>
                  <div className="font-medium text-gray-700">Force</div>
                  <div className="text-gray-600">{currentInsight.motionDescription.force}</div>
                </div>
                <div>
                  <div className="font-medium text-gray-700">Spatial</div>
                  <div className="text-gray-600">{currentInsight.motionDescription.spatialExtent}</div>
                </div>
                <div>
                  <div className="font-medium text-gray-700">Temporal</div>
                  <div className="text-gray-600">{currentInsight.motionDescription.temporalAspect}</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-sm text-gray-500">No motion described</div>
          )}
        </div>

        {/* Pattern */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 col-span-2">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">🌀 Geometric Pattern</h3>
          <div className="space-y-3">
            <div>
              <span className="font-medium text-gray-700">Primary: </span>
              <span className="text-gray-800">{currentInsight.patternAnalysis.primaryPattern}</span>
              {currentInsight.patternAnalysis.secondaryPatterns.length > 0 && (
                <>
                  <span className="text-gray-600"> + </span>
                  <span className="text-gray-600">
                    {currentInsight.patternAnalysis.secondaryPatterns.join(', ')}
                  </span>
                </>
              )}
            </div>
            {currentInsight.patternAnalysis.description && (
              <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                {currentInsight.patternAnalysis.description}
              </div>
            )}
            {currentInsight.patternAnalysis.naturalExamples.length > 0 && (
              <div>
                <span className="text-sm font-medium text-gray-700">Natural Examples: </span>
                <span className="text-sm text-gray-600">
                  {currentInsight.patternAnalysis.naturalExamples.join(', ')}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Translations */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 col-span-2">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">📖 Translation Comparison</h3>
          <div className="space-y-3">
            <div>
              <div className="text-sm font-medium text-gray-700">Standard</div>
              <div className="text-sm text-gray-600">
                {currentInsight.translations.standard || '—'}
              </div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-700">Structural (RSM)</div>
              <div className="text-sm text-gray-600">
                {currentInsight.translations.structural || '—'}
              </div>
            </div>
            <div className="bg-purple-50 p-3 rounded">
              <div className="text-sm font-medium text-purple-900">Motion-Based (New!)</div>
              <div className="text-sm text-purple-800 font-medium">
                {currentInsight.translations.motion || '—'}
              </div>
            </div>
          </div>
        </div>

        {/* Insights & Hypotheses */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">💡 Insights</h3>
          {currentInsight.insights.length > 0 ? (
            <ul className="space-y-2">
              {currentInsight.insights.map((insight, i) => (
                <li key={i} className="text-sm text-gray-700">
                  • {insight}
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-sm text-gray-500">No insights recorded</div>
          )}
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">🔬 Hypotheses</h3>
          {currentInsight.hypotheses.length > 0 ? (
            <ul className="space-y-2">
              {currentInsight.hypotheses.map((hypothesis, i) => (
                <li key={i} className="text-sm text-gray-700">
                  • {hypothesis}
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-sm text-gray-500">No hypotheses generated</div>
          )}
        </div>
      </div>

      {/* Confidence */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Confidence Level</h3>
            <p className="text-sm text-gray-600">
              How confident are you in this motion-based reading?
            </p>
          </div>
          <div className="text-3xl font-bold text-purple-600">
            {Math.round(currentInsight.confidence * 100)}%
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={handleSave}
          className="flex-1 px-6 py-4 bg-green-600 text-white text-lg font-semibold rounded-lg hover:bg-green-700 transition-colors"
        >
          ✓ Save Insight
        </button>
        <button
          onClick={handleSaveAndNew}
          className="flex-1 px-6 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors"
        >
          Save & Analyze Another →
        </button>
      </div>

      {/* Warning for incomplete */}
      {completionPercent < 70 && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="text-sm font-medium text-amber-900 mb-1">⚠️ Analysis Incomplete</div>
          <div className="text-sm text-amber-800">
            Some sections haven't been filled out yet. You can save now, but consider completing
            all steps for a more thorough analysis.
          </div>
        </div>
      )}
    </div>
  );
};
