import React, { useState } from 'react';
import { useMotionStore } from '../../store/useMotionStore';

export const InsightsRecorder: React.FC = () => {
  const { currentInsight, addInsightNote, addHypothesis, updateTranslations, updateConfidence } =
    useMotionStore();
  const [newInsight, setNewInsight] = useState('');
  const [newHypothesis, setNewHypothesis] = useState('');
  const [translations, setTranslations] = useState({
    standard: '',
    structural: '',
    motion: '',
  });

  React.useEffect(() => {
    if (currentInsight) {
      setTranslations(currentInsight.translations);
    }
  }, [currentInsight]);

  const handleAddInsight = () => {
    if (newInsight.trim()) {
      addInsightNote(newInsight.trim());
      setNewInsight('');
    }
  };

  const handleAddHypothesis = () => {
    if (newHypothesis.trim()) {
      addHypothesis(newHypothesis.trim());
      setNewHypothesis('');
    }
  };

  const handleSaveTranslations = () => {
    updateTranslations(translations);
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-purple-900 mb-2">
          <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
          Insights & Hypotheses
        </h2>
        <p className="text-sm text-purple-800">
          Record your insights and generate testable hypotheses about this character.
        </p>
      </div>

      {/* Translation Comparison */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-4">
        <h3 className="text-lg font-semibold text-gray-900">Translation Comparison</h3>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Standard Translation
          </label>
          <input
            type="text"
            value={translations.standard}
            onChange={(e) => setTranslations({ ...translations, standard: e.target.value })}
            onBlur={handleSaveTranslations}
            placeholder="Traditional dictionary meaning..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Structural Reading (RSM)
          </label>
          <input
            type="text"
            value={translations.structural}
            onChange={(e) => setTranslations({ ...translations, structural: e.target.value })}
            onBlur={handleSaveTranslations}
            placeholder="Your previous structural interpretation..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Motion-Based Reading (New!)
          </label>
          <input
            type="text"
            value={translations.motion}
            onChange={(e) => setTranslations({ ...translations, motion: e.target.value })}
            onBlur={handleSaveTranslations}
            placeholder="What does this mean as a geometric operation?"
            className="w-full px-4 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500 bg-purple-50"
          />
        </div>
      </div>

      {/* Insights */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Insights</h3>
        <div className="space-y-3">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newInsight}
              onChange={(e) => setNewInsight(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddInsight()}
              placeholder="What did you discover about this character?"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            />
            <button
              onClick={handleAddInsight}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Add
            </button>
          </div>

          <div className="space-y-2">
            {currentInsight.insights.map((insight, i) => (
              <div key={i} className="p-3 bg-purple-50 rounded-lg text-sm text-gray-700">
                💡 {insight}
              </div>
            ))}
            {currentInsight.insights.length === 0 && (
              <div className="text-center py-4 text-gray-500 text-sm">
                No insights recorded yet
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Hypotheses */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Testable Hypotheses</h3>
        <div className="space-y-3">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newHypothesis}
              onChange={(e) => setNewHypothesis(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddHypothesis()}
              placeholder="What hypothesis can you test based on this reading?"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            />
            <button
              onClick={handleAddHypothesis}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Add
            </button>
          </div>

          <div className="space-y-2">
            {currentInsight.hypotheses.map((hypothesis, i) => (
              <div key={i} className="p-3 bg-blue-50 rounded-lg text-sm text-gray-700">
                🔬 {hypothesis}
              </div>
            ))}
            {currentInsight.hypotheses.length === 0 && (
              <div className="text-center py-4 text-gray-500 text-sm">
                No hypotheses generated yet
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Confidence */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-4">
          Overall Confidence in This Reading: {Math.round(currentInsight.confidence * 100)}%
        </label>
        <input
          type="range"
          min="0"
          max="100"
          value={currentInsight.confidence * 100}
          onChange={(e) => updateConfidence(parseInt(e.target.value) / 100)}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>Speculative</span>
          <span>Moderately Confident</span>
          <span>Very Confident</span>
        </div>
      </div>

      {/* Tip */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="text-sm font-medium text-amber-900 mb-2">💡 Tip:</div>
        <div className="text-sm text-amber-800">
          Good hypotheses are specific and testable. For example: "If 利 means 'efficient cutting
          motion', it should appear frequently in contexts involving tools, harvest, or optimization."
        </div>
      </div>
    </div>
  );
};
