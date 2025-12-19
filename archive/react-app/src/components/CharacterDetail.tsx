import { useAppStore } from '../store/useAppStore';
import { getRadicalsForChar, getRadicalName } from '../utils/radicalDetector';
import { useEffect } from 'react';

export function CharacterDetail() {
  const { selectedCharacter, selectedCharacterData, selectCharacter } = useAppStore();

  // Handle ESC key to close panel
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        selectCharacter(null);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectCharacter]);

  if (!selectedCharacter || !selectedCharacterData) {
    return null;
  }

  const radicals = getRadicalsForChar(selectedCharacter.char);
  const occurrences = selectedCharacterData.occurrences;

  const handleOccurrenceClick = (chapter: number, position: number) => {
    // Scroll to the cell in the grid
    const cell = document.querySelector(
      `table tbody tr:nth-child(${position}) td:nth-child(${chapter + 1})`
    );

    if (cell) {
      cell.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });

      // Briefly highlight the cell
      cell.classList.add('ring-2', 'ring-yellow-400');
      setTimeout(() => {
        cell.classList.remove('ring-2', 'ring-yellow-400');
      }, 2000);
    }
  };

  return (
    <div className="fixed right-0 top-0 h-full w-80 bg-gray-800 shadow-2xl border-l border-gray-700 overflow-y-auto z-20">
      <div className="p-4">
        {/* Header */}
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-4xl font-bold chinese-char mb-2">
              {selectedCharacter.char}
            </h2>
            <p className="text-gray-400">{selectedCharacterData.pinyin}</p>
          </div>
          <button
            onClick={() => selectCharacter(null)}
            className="text-gray-400 hover:text-white text-2xl leading-none"
            title="Close (ESC)"
          >
            ×
          </button>
        </div>

        {/* Location */}
        <div className="mb-4 p-3 bg-gray-700 rounded">
          <p className="text-sm text-gray-300">
            <span className="font-semibold">Location:</span> Chapter {selectedCharacter.chapter}, Position {selectedCharacter.position}
          </p>
        </div>

        {/* Radicals */}
        {radicals.length > 0 && (
          <div className="mb-4">
            <h3 className="text-sm font-semibold text-gray-300 mb-2">Radicals</h3>
            <div className="flex flex-wrap gap-2">
              {radicals.map(radical => (
                <span
                  key={radical}
                  className="px-2 py-1 bg-gray-700 rounded text-sm"
                  title={getRadicalName(radical)}
                >
                  {radical}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Occurrences */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-2">
            All Occurrences ({occurrences.length})
          </h3>
          <div className="space-y-1 max-h-96 overflow-y-auto">
            {occurrences.map((occurrence, index) => {
              const isCurrent =
                occurrence.chapter === selectedCharacter.chapter &&
                occurrence.position === selectedCharacter.position;

              return (
                <button
                  key={index}
                  onClick={() => handleOccurrenceClick(occurrence.chapter, occurrence.position)}
                  className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                    isCurrent
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  }`}
                >
                  Chapter {occurrence.chapter}, Position {occurrence.position}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
