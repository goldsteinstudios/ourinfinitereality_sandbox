import { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { RADICALS } from '../utils/radicalDetector';

interface HeaderProps {
  viewMode: 'grid' | 'analysis' | 'motion';
  setViewMode: (mode: 'grid' | 'analysis' | 'motion') => void;
}

export function Header({ viewMode, setViewMode }: HeaderProps) {
  const {
    selectedRadicals,
    highlightMode,
    searchQuery,
    searchResults,
    toggleRadical,
    clearRadicals,
    setHighlightMode,
    performSearch,
    data,
  } = useAppStore();

  const [showRadicalMenu, setShowRadicalMenu] = useState(false);
  const [searchInput, setSearchInput] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    performSearch(searchInput);
  };

  const scrollToResult = (chapter: number, position: number) => {
    const cell = document.querySelector(
      `table tbody tr:nth-child(${position}) td:nth-child(${chapter + 1})`
    );

    if (cell) {
      cell.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      cell.classList.add('ring-2', 'ring-yellow-400');
      setTimeout(() => {
        cell.classList.remove('ring-2', 'ring-yellow-400');
      }, 2000);
    }
  };

  const totalCharacters = data?.characters.length || 0;

  return (
    <header className="bg-gray-800 border-b border-gray-700 p-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Dao De Jing Pattern Analyzer</h1>
          <p className="text-sm text-gray-400">
            {totalCharacters.toLocaleString()} characters across 81 chapters
          </p>
        </div>

        {/* View Mode Toggle */}
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('grid')}
            className={`px-4 py-2 rounded transition-colors ${
              viewMode === 'grid'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Character Grid
          </button>
          <button
            onClick={() => setViewMode('analysis')}
            className={`px-4 py-2 rounded transition-colors ${
              viewMode === 'analysis'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Analysis Tools
          </button>
          <button
            onClick={() => setViewMode('motion')}
            className={`px-4 py-2 rounded transition-colors ${
              viewMode === 'motion'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Motion Decoder
          </button>
        </div>
      </div>

      <div className="flex gap-4 flex-wrap items-start">
        {/* Radical Highlighting */}
        <div className="relative">
          <button
            onClick={() => setShowRadicalMenu(!showRadicalMenu)}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-medium transition-colors"
          >
            Highlight Radicals {selectedRadicals.length > 0 && `(${selectedRadicals.length})`}
          </button>

          {showRadicalMenu && (
            <div className="absolute top-full left-0 mt-2 w-64 bg-gray-700 rounded shadow-xl border border-gray-600 z-30 p-3">
              <div className="mb-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-semibold">Select Radicals</span>
                  {selectedRadicals.length > 0 && (
                    <button
                      onClick={clearRadicals}
                      className="text-xs text-blue-400 hover:text-blue-300"
                    >
                      Clear All
                    </button>
                  )}
                </div>
                <div className="space-y-1">
                  {RADICALS.map(radical => (
                    <label
                      key={radical.radical}
                      className="flex items-center gap-2 cursor-pointer hover:bg-gray-600 p-1 rounded"
                    >
                      <input
                        type="checkbox"
                        checked={selectedRadicals.includes(radical.radical)}
                        onChange={() => toggleRadical(radical.radical)}
                        className="rounded"
                      />
                      <span
                        className="w-4 h-4 rounded"
                        style={{ backgroundColor: radical.color }}
                      />
                      <span className="text-sm">{radical.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {selectedRadicals.length > 1 && (
                <div className="pt-3 border-t border-gray-600">
                  <span className="text-xs font-semibold block mb-2">Mode</span>
                  <div className="space-y-1">
                    <label className="flex items-center gap-2 cursor-pointer hover:bg-gray-600 p-1 rounded">
                      <input
                        type="radio"
                        checked={highlightMode === 'union'}
                        onChange={() => setHighlightMode('union')}
                      />
                      <span className="text-xs">Any radical (Union)</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer hover:bg-gray-600 p-1 rounded">
                      <input
                        type="radio"
                        checked={highlightMode === 'intersection'}
                        onChange={() => setHighlightMode('intersection')}
                      />
                      <span className="text-xs">All radicals (Intersection)</span>
                    </label>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Search */}
        <form onSubmit={handleSearch} className="flex gap-2 flex-1 max-w-md">
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search character or pinyin..."
            className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm font-medium transition-colors"
          >
            Search
          </button>
        </form>

        {/* Search Results */}
        {searchQuery && (
          <div className="w-full mt-2">
            <div className="bg-gray-700 rounded p-3">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-semibold">
                  Search Results: {searchResults.length} found
                </span>
                <button
                  onClick={() => {
                    performSearch('');
                    setSearchInput('');
                  }}
                  className="text-xs text-gray-400 hover:text-white"
                >
                  Clear
                </button>
              </div>
              {searchResults.length > 0 && (
                <div className="space-y-1 max-h-40 overflow-y-auto">
                  {searchResults.slice(0, 50).map((result, index) => (
                    <button
                      key={index}
                      onClick={() => scrollToResult(result.chapter, result.position)}
                      className="w-full text-left px-2 py-1 bg-gray-600 hover:bg-gray-500 rounded text-sm transition-colors"
                    >
                      <span className="chinese-char font-semibold">{result.char}</span> ({result.pinyin})
                      - Ch. {result.chapter}, Pos. {result.position}
                    </button>
                  ))}
                  {searchResults.length > 50 && (
                    <p className="text-xs text-gray-400 pt-2">
                      Showing first 50 of {searchResults.length} results
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
