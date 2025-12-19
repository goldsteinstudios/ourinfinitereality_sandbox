import React, { useMemo } from 'react';
import { useMotionStore } from '../../store/useMotionStore';
import { useAppStore } from '../../store/useAppStore';

export const ContextTester: React.FC = () => {
  const { currentInsight } = useMotionStore();
  const { characterData, characters } = useAppStore();

  const occurrences = useMemo(() => {
    if (!currentInsight) return [];
    const data = characterData.get(currentInsight.character);
    return data?.occurrences.slice(0, 10) || []; // Show first 10
  }, [currentInsight, characterData]);

  const getContext = (chapter: number, position: number) => {
    const before: string[] = [];
    const after: string[] = [];

    // Get 3 characters before and after
    for (let i = -3; i <= 3; i++) {
      if (i === 0) continue;
      const char = characters[position + i]?.[chapter - 1];
      if (char) {
        if (i < 0) before.push(char.char);
        else after.push(char.char);
      }
    }

    return { before: before.join(''), after: after.join('') };
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      <div className="bg-teal-50 border border-teal-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-teal-900 mb-2">
          <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
          Context Testing
        </h2>
        <p className="text-sm text-teal-800">
          Does your motion reading make sense in actual usage? Review contexts from the text.
        </p>
      </div>

      {/* Motion Reading Summary */}
      <div className="bg-white rounded-lg border-2 border-teal-300 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Motion Reading:</h3>
        <div className="space-y-3">
          {currentInsight.physicalAction && (
            <div>
              <div className="text-sm font-medium text-gray-700">Physical Action:</div>
              <div className="text-sm text-gray-600 italic">{currentInsight.physicalAction}</div>
            </div>
          )}
          {currentInsight.translations.motion && (
            <div>
              <div className="text-sm font-medium text-gray-700">Motion Translation:</div>
              <div className="text-sm text-gray-600 italic">
                {currentInsight.translations.motion}
              </div>
            </div>
          )}
          <div>
            <div className="text-sm font-medium text-gray-700">Pattern:</div>
            <div className="text-sm text-gray-600">
              {currentInsight.patternAnalysis.primaryPattern}
              {currentInsight.patternAnalysis.secondaryPatterns.length > 0 &&
                ` (+ ${currentInsight.patternAnalysis.secondaryPatterns.join(', ')})`}
            </div>
          </div>
        </div>
      </div>

      {/* Occurrences */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Usage Examples (showing {occurrences.length} of {characterData.get(currentInsight.character)?.occurrences.length || 0})
        </h3>

        <div className="space-y-4">
          {occurrences.map((occ, index) => {
            const context = getContext(occ.chapter, occ.position);
            return (
              <div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm font-medium text-gray-700">
                    Chapter {occ.chapter}, Position {occ.position}
                  </div>
                </div>
                <div className="flex items-center justify-center text-2xl font-serif space-x-1">
                  <span className="text-gray-400">{context.before}</span>
                  <span className="text-teal-600 font-bold px-2 bg-teal-100 rounded">
                    {currentInsight.character}
                  </span>
                  <span className="text-gray-400">{context.after}</span>
                </div>
                <div className="mt-3 text-sm text-gray-600">
                  <strong>Question:</strong> Does your motion reading fit here?
                </div>
              </div>
            );
          })}
        </div>

        {occurrences.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No occurrences found for this character.
          </div>
        )}
      </div>

      {/* Coherence Assessment */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-4">
          Overall Coherence: How well does your motion reading fit the actual usage?
        </label>
        <div className="text-center py-4">
          <div className="text-4xl font-bold text-gray-400 mb-2">Coming Soon</div>
          <div className="text-sm text-gray-500">
            Manual coherence scoring will be added in next iteration
          </div>
        </div>
      </div>

      {/* Tip */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="text-sm font-medium text-amber-900 mb-2">💡 Tip:</div>
        <div className="text-sm text-amber-800">
          If your motion reading doesn't fit most contexts, you may need to revise your
          interpretation. Go back and adjust the motion description or pattern identification.
        </div>
      </div>
    </div>
  );
};
