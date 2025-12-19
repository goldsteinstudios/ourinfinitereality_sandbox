import React, { useState, useMemo } from 'react';
import { useMotionStore } from '../../store/useMotionStore';
import { useAppStore } from '../../store/useAppStore';

export const CharacterSelector: React.FC = () => {
  const { selectCharacter, getAllInsights } = useMotionStore();
  const { characterData } = useAppStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterMode, setFilterMode] = useState<'all' | 'analyzed' | 'unanalyzed'>('all');

  const existingInsights = useMemo(() => {
    return new Set(getAllInsights().map((i) => i.character));
  }, [getAllInsights]);

  // Get all unique characters from the data
  const allCharacters = useMemo(() => {
    const chars = Array.from(characterData.entries()).map(([char, data]) => ({
      character: char,
      pinyin: data.pinyin,
      count: data.occurrences.length,
      analyzed: existingInsights.has(char),
    }));

    // Filter by analysis status
    let filtered = chars;
    if (filterMode === 'analyzed') {
      filtered = chars.filter((c) => c.analyzed);
    } else if (filterMode === 'unanalyzed') {
      filtered = chars.filter((c) => !c.analyzed);
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (c) =>
          c.character.includes(query) ||
          c.pinyin.toLowerCase().includes(query)
      );
    }

    // Sort by frequency
    return filtered.sort((a, b) => b.count - a.count);
  }, [characterData, searchQuery, filterMode, existingInsights]);

  const stats = useMemo(() => {
    return {
      total: Array.from(characterData.keys()).length,
      analyzed: existingInsights.size,
      unanalyzed: Array.from(characterData.keys()).length - existingInsights.size,
    };
  }, [characterData, existingInsights]);

  return (
    <div className="space-y-6">
      {/* Introduction */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-2">
          🔍 Decode Characters as Geometric Operations
        </h2>
        <p className="text-sm text-blue-800">
          This tool helps you decode Chinese characters as encoded physical motions and geometric
          patterns. Select a character from the Dao De Jing to begin the analysis.
        </p>
        <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
          <div className="bg-white rounded p-3">
            <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
            <div className="text-gray-600">Total Characters</div>
          </div>
          <div className="bg-white rounded p-3">
            <div className="text-2xl font-bold text-green-600">{stats.analyzed}</div>
            <div className="text-gray-600">Analyzed</div>
          </div>
          <div className="bg-white rounded p-3">
            <div className="text-2xl font-bold text-gray-600">{stats.unanalyzed}</div>
            <div className="text-gray-600">Remaining</div>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search Characters
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by character or pinyin..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Filter</label>
          <div className="flex space-x-2">
            {(['all', 'analyzed', 'unanalyzed'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setFilterMode(mode)}
                className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                  filterMode === mode
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Character Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-gray-700">
            {allCharacters.length} character{allCharacters.length !== 1 ? 's' : ''} found
          </h3>
        </div>

        <div className="grid grid-cols-8 gap-3 max-h-96 overflow-y-auto p-4 bg-white rounded-lg border border-gray-200">
          {allCharacters.map(({ character, pinyin, count, analyzed }) => (
            <button
              key={character}
              onClick={() => selectCharacter(character, pinyin)}
              className={`
                relative group flex flex-col items-center justify-center p-4 rounded-lg
                transition-all hover:scale-105 hover:shadow-lg
                ${
                  analyzed
                    ? 'bg-green-50 border-2 border-green-500 hover:bg-green-100'
                    : 'bg-gray-50 border border-gray-200 hover:bg-blue-50 hover:border-blue-400'
                }
              `}
            >
              {analyzed && (
                <div className="absolute top-1 right-1 w-2 h-2 bg-green-500 rounded-full" />
              )}
              <div className="text-3xl font-serif mb-1">{character}</div>
              <div className="text-xs text-gray-600">{pinyin}</div>
              <div className="text-xs text-gray-400 mt-1">{count}×</div>

              {/* Tooltip on hover */}
              <div className="absolute bottom-full mb-2 hidden group-hover:block z-10">
                <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                  {analyzed ? '✓ Already analyzed' : 'Click to analyze'}
                </div>
              </div>
            </button>
          ))}
        </div>

        {allCharacters.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No characters found matching your criteria.
          </div>
        )}
      </div>

      {/* Example: 利 (scythe) */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
        <h3 className="text-sm font-semibold text-amber-900 mb-2">💡 Example: 利 (lì)</h3>
        <p className="text-sm text-amber-800 mb-3">
          Try starting with <span className="font-bold text-lg">利</span>. Traditional translation:
          "benefit, advantage". But when you imagine the motion...
        </p>
        <div className="bg-white rounded p-4 text-sm text-gray-700 space-y-2">
          <div>
            <strong>Radicals:</strong> 禾 (grain) + knife/blade tool
          </div>
          <div>
            <strong>Imagine:</strong> You're standing in a grain field. You swing a scythe in a
            circular arc.
          </div>
          <div>
            <strong>Pattern:</strong> The blade traces a spiral as you move through the field,
            creating a φ-ratio pattern.
          </div>
          <div>
            <strong>Motion Reading:</strong> "The efficient cutting motion that creates optimal
            pattern distribution"
          </div>
        </div>
        <button
          onClick={() => selectCharacter('利', 'lì')}
          className="mt-4 w-full px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
        >
          Analyze 利 (lì) →
        </button>
      </div>
    </div>
  );
};
