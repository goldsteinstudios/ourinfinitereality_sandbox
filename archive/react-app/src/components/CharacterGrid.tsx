import { useAppStore } from '../store/useAppStore';
import { hasRadical, getRadicalColor } from '../utils/radicalDetector';
import type { Character } from '../types';

export function CharacterGrid() {
  const { data, selectedRadicals, highlightMode, selectCharacter } = useAppStore();

  if (!data) {
    return null;
  }

  const { grid } = data;
  const maxRows = Math.max(...grid.map(chapter => chapter.length));

  const shouldHighlight = (char: Character | null): boolean => {
    if (!char || selectedRadicals.length === 0) return false;

    const charRadicals = selectedRadicals.filter(radical => hasRadical(char.char, radical));

    if (highlightMode === 'union') {
      return charRadicals.length > 0;
    } else {
      // intersection mode
      return charRadicals.length === selectedRadicals.length;
    }
  };

  const getHighlightColor = (char: Character | null): string | null => {
    if (!char || !shouldHighlight(char)) return null;

    // If only one radical is selected, use its color
    if (selectedRadicals.length === 1) {
      return getRadicalColor(selectedRadicals[0]);
    }

    // For multiple radicals, use a gradient or the first matching radical's color
    const matchingRadical = selectedRadicals.find(radical => hasRadical(char.char, radical));
    return matchingRadical ? getRadicalColor(matchingRadical) : null;
  };

  const handleCharacterClick = (char: Character | null) => {
    if (char) {
      selectCharacter(char);
    }
  };

  return (
    <div className="overflow-auto h-full">
      <table className="border-collapse text-sm">
        <thead className="sticky top-0 bg-gray-800 z-10">
          <tr>
            <th className="border border-gray-600 px-2 py-1 text-gray-300 min-w-[50px] bg-gray-800">
              Row
            </th>
            {Array.from({ length: 81 }, (_, i) => i + 1).map(chapterNum => (
              <th
                key={chapterNum}
                className="border border-gray-600 px-2 py-1 text-gray-300 min-w-[40px] bg-gray-800"
              >
                {chapterNum}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: maxRows }, (_, rowIndex) => (
            <tr key={rowIndex}>
              <td className="border border-gray-600 px-2 py-1 text-gray-400 text-xs text-center bg-gray-800 sticky left-0">
                {rowIndex + 1}
              </td>
              {grid.map((chapter, chapterIndex) => {
                const char = chapter[rowIndex] || null;
                const highlighted = shouldHighlight(char);
                const highlightColor = getHighlightColor(char);

                return (
                  <td
                    key={chapterIndex}
                    className={`border border-gray-700 px-2 py-1 text-center cursor-pointer transition-colors ${
                      char ? 'hover:bg-gray-700' : 'bg-gray-900'
                    }`}
                    style={{
                      backgroundColor: highlighted && highlightColor
                        ? `${highlightColor}40`
                        : undefined,
                      borderColor: highlighted && highlightColor
                        ? highlightColor
                        : undefined,
                    }}
                    onClick={() => handleCharacterClick(char)}
                    title={char ? `${char.char} (${char.pinyin}) - Chapter ${char.chapter}, Position ${char.position}` : ''}
                  >
                    <span className="chinese-char text-base">
                      {char?.char || ''}
                    </span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
