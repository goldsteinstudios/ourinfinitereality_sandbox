import React, { useState, useEffect } from 'react';
import { useMotionStore } from '../../store/useMotionStore';

export const RadicalBreakdown: React.FC = () => {
  const { currentInsight, updateRadicals } = useMotionStore();
  const [radicals, setRadicals] = useState<string[]>([]);
  const [radicalInput, setRadicalInput] = useState('');
  const [meanings, setMeanings] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    if (currentInsight) {
      setRadicals(currentInsight.radicals);
      setMeanings(currentInsight.radicalMeanings);
    }
  }, [currentInsight]);

  const addRadical = () => {
    if (radicalInput && !radicals.includes(radicalInput)) {
      const newRadicals = [...radicals, radicalInput];
      setRadicals(newRadicals);
      updateRadicals(newRadicals, meanings);
      setRadicalInput('');
    }
  };

  const removeRadical = (radical: string) => {
    const newRadicals = radicals.filter((r) => r !== radical);
    const newMeanings = { ...meanings };
    delete newMeanings[radical];
    setRadicals(newRadicals);
    setMeanings(newMeanings);
    updateRadicals(newRadicals, newMeanings);
  };

  const updateMeaning = (radical: string, meaning: string) => {
    const newMeanings = { ...meanings, [radical]: meaning };
    setMeanings(newMeanings);
    updateRadicals(radicals, newMeanings);
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-blue-900">
            <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
            Radical Breakdown
          </h2>
        </div>
        <p className="text-sm text-blue-800">
          Break down the character into its component radicals. Each radical may hint at a
          physical element or action.
        </p>
      </div>

      {/* Add Radicals */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Add Radical</label>
        <div className="flex space-x-2">
          <input
            type="text"
            value={radicalInput}
            onChange={(e) => setRadicalInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addRadical()}
            placeholder="Enter radical character..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={addRadical}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Add
          </button>
        </div>
      </div>

      {/* Radical List */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Component Radicals ({radicals.length})
        </h3>

        {radicals.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No radicals added yet. Add radicals above to begin analysis.
          </div>
        ) : (
          <div className="space-y-4">
            {radicals.map((radical) => (
              <div
                key={radical}
                className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg"
              >
                <div className="text-4xl font-serif">{radical}</div>
                <div className="flex-1">
                  <input
                    type="text"
                    value={meanings[radical] || ''}
                    onChange={(e) => updateMeaning(radical, e.target.value)}
                    placeholder="What does this radical mean? (e.g., 'grain', 'hand', 'water')"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <button
                  onClick={() => removeRadical(radical)}
                  className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Helpful Tips */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="text-sm font-medium text-amber-900 mb-2">💡 Tips:</div>
        <ul className="text-sm text-amber-800 space-y-1 list-disc list-inside">
          <li>Look for tool-related radicals: 刀 (knife), 手 (hand), 木 (wood)</li>
          <li>Note position and orientation of each component</li>
          <li>Consider what physical object or action each radical suggests</li>
        </ul>
      </div>
    </div>
  );
};
