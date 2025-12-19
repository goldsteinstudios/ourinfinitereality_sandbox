import { useEffect, useState } from 'react';
import { useAnalysisStore } from '../../store/useAnalysisStore';
import { getTopPairs, exportMatrixToCSV } from '../../utils/coOccurrenceCalculator';
import { exportCoOccurrenceMatrix } from '../../utils/reportGenerator';

export function CoOccurrenceMatrix() {
  const {
    matrix,
    matrixLoading,
    proximityThreshold,
    minFrequency,
    generateMatrix,
    setProximityThreshold,
    setMinFrequency,
    pairToContext,
  } = useAnalysisStore();

  const [viewMode, setViewMode] = useState<'top-pairs' | 'full-matrix'>('top-pairs');
  const [topN, setTopN] = useState(50);

  useEffect(() => {
    if (!matrix) {
      generateMatrix();
    }
  }, [matrix, generateMatrix]);

  if (matrixLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Calculating co-occurrence matrix...</p>
        </div>
      </div>
    );
  }

  if (!matrix) {
    return (
      <div className="text-center p-8">
        <p className="text-gray-400 mb-4">No matrix data available</p>
        <button
          onClick={generateMatrix}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded"
        >
          Generate Matrix
        </button>
      </div>
    );
  }

  const topPairs = getTopPairs(matrix, topN);

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="p-4 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-4 flex-wrap">
          <div>
            <label className="text-sm text-gray-400 block mb-1">
              Proximity Threshold
            </label>
            <input
              type="number"
              min="2"
              max="20"
              value={proximityThreshold}
              onChange={(e) => setProximityThreshold(Number(e.target.value))}
              className="w-20 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-1">
              Min Frequency
            </label>
            <input
              type="number"
              min="1"
              max="50"
              value={minFrequency}
              onChange={(e) => setMinFrequency(Number(e.target.value))}
              className="w-20 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-1">View Mode</label>
            <select
              value={viewMode}
              onChange={(e) => setViewMode(e.target.value as typeof viewMode)}
              className="px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
            >
              <option value="top-pairs">Top Pairs</option>
              <option value="full-matrix">Full Matrix</option>
            </select>
          </div>

          {viewMode === 'top-pairs' && (
            <div>
              <label className="text-sm text-gray-400 block mb-1">Show Top</label>
              <input
                type="number"
                min="10"
                max="200"
                value={topN}
                onChange={(e) => setTopN(Number(e.target.value))}
                className="w-20 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
              />
            </div>
          )}

          <div className="ml-auto flex gap-2">
            <button
              onClick={() => exportCoOccurrenceMatrix(matrix, 'csv')}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
            >
              Export CSV
            </button>
            <button
              onClick={() => exportCoOccurrenceMatrix(matrix, 'json')}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
            >
              Export JSON
            </button>
          </div>
        </div>

        <div className="mt-2 text-sm text-gray-400">
          {matrix.characters.length} unique characters, {topPairs.length} pairs found
        </div>
      </div>

      {/* Matrix Display */}
      <div className="flex-1 overflow-auto p-4">
        {viewMode === 'top-pairs' ? (
          <TopPairsView pairs={topPairs} onPairClick={pairToContext} />
        ) : (
          <div className="text-gray-400 text-center p-8">
            Full matrix view with {matrix.characters.length}×{matrix.characters.length} grid
            would be implemented here. For large datasets, the Top Pairs view is recommended.
          </div>
        )}
      </div>
    </div>
  );
}

interface TopPairsViewProps {
  pairs: Array<{ char1: string; char2: string; count: number }>;
  onPairClick: (char1: string, char2: string) => void;
}

function TopPairsView({ pairs, onPairClick }: TopPairsViewProps) {
  const [sortBy, setSortBy] = useState<'frequency' | 'alpha'>('frequency');
  const [filterChar, setFilterChar] = useState('');

  let displayPairs = [...pairs];

  // Filter
  if (filterChar) {
    displayPairs = displayPairs.filter(
      p => p.char1.includes(filterChar) || p.char2.includes(filterChar)
    );
  }

  // Sort
  if (sortBy === 'alpha') {
    displayPairs.sort((a, b) => a.char1.localeCompare(b.char1));
  }

  // Calculate color intensity based on frequency
  const maxCount = Math.max(...pairs.map(p => p.count), 1);
  const getColor = (count: number) => {
    const intensity = Math.min(count / maxCount, 1);
    const r = Math.floor(59 + intensity * 180); // 59 to 239
    const g = Math.floor(130 + intensity * 100); // 130 to 230
    const b = Math.floor(246 - intensity * 50); // 246 to 196
    return `rgb(${r}, ${g}, ${b})`;
  };

  return (
    <div>
      <div className="flex gap-4 mb-4">
        <div>
          <label className="text-sm text-gray-400 block mb-1">Sort By</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
            className="px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
          >
            <option value="frequency">Frequency</option>
            <option value="alpha">Alphabetical</option>
          </select>
        </div>

        <div className="flex-1">
          <label className="text-sm text-gray-400 block mb-1">
            Filter by Character
          </label>
          <input
            type="text"
            value={filterChar}
            onChange={(e) => setFilterChar(e.target.value)}
            placeholder="Enter character..."
            className="w-full px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
        {displayPairs.map((pair, index) => (
          <button
            key={`${pair.char1}-${pair.char2}-${index}`}
            onClick={() => onPairClick(pair.char1, pair.char2)}
            className="flex items-center justify-between p-3 rounded transition-all hover:ring-2 hover:ring-blue-400"
            style={{
              backgroundColor: getColor(pair.count),
            }}
          >
            <div className="flex items-center gap-2">
              <span className="text-2xl chinese-char font-bold text-gray-900">
                {pair.char1}
              </span>
              <span className="text-gray-700">↔</span>
              <span className="text-2xl chinese-char font-bold text-gray-900">
                {pair.char2}
              </span>
            </div>
            <span className="text-sm font-semibold text-gray-900 bg-white/30 px-2 py-1 rounded">
              {pair.count}
            </span>
          </button>
        ))}
      </div>

      {displayPairs.length === 0 && (
        <div className="text-center text-gray-400 py-8">
          No pairs match the filter
        </div>
      )}
    </div>
  );
}
