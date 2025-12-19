import { useState } from 'react';
import { useAnalysisStore } from '../../store/useAnalysisStore';
import type { Character } from '../../types';

export function ContextViewer() {
  const {
    contexts,
    currentContextIndex,
    contextWindowSize,
    contextHighlightChars,
    setContextWindowSize,
    nextContext,
    prevContext,
    goToContext,
    addContextAnnotation,
    setContextHighlight,
    contextToContrast,
  } = useAnalysisStore();

  const [note, setNote] = useState('');
  const [tags, setTags] = useState('');
  const [highlightInput, setHighlightInput] = useState('');

  if (contexts.length === 0) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <p className="text-gray-400 text-lg mb-4">No context loaded</p>
          <p className="text-gray-500 text-sm">
            Click a character pair in the Co-occurrence Matrix or search for a character
          </p>
        </div>
      </div>
    );
  }

  const currentContext = contexts[currentContextIndex];
  const progress = `${currentContextIndex + 1} / ${contexts.length}`;

  const renderCharacter = (char: Character, isCenter: boolean = false) => {
    const isHighlighted = contextHighlightChars.includes(char.char);

    return (
      <span
        key={`${char.chapter}-${char.position}`}
        className={`chinese-char text-xl ${
          isCenter
            ? 'font-bold text-yellow-400 mx-1 text-2xl'
            : isHighlighted
            ? 'text-blue-400 font-semibold'
            : 'text-gray-300'
        }`}
        title={`${char.char} (${char.pinyin}) - Ch${char.chapter}:${char.position}`}
      >
        {char.char}
      </span>
    );
  };

  const handleAddAnnotation = () => {
    if (note.trim()) {
      const tagArray = tags.split(',').map(t => t.trim()).filter(t => t);
      addContextAnnotation(note, tagArray);
      setNote('');
      setTags('');
    }
  };

  const handleAddHighlight = () => {
    if (highlightInput.trim()) {
      const newHighlights = [...contextHighlightChars, ...highlightInput.split('').filter(c => c.trim())];
      setContextHighlight(Array.from(new Set(newHighlights)));
      setHighlightInput('');
    }
  };

  const handleCreateContrast = () => {
    if (contextHighlightChars.length >= 2) {
      contextToContrast(contextHighlightChars[0], contextHighlightChars[1]);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="p-4 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <div>
              <label className="text-sm text-gray-400 block mb-1">
                Window Size
              </label>
              <input
                type="number"
                min="3"
                max="15"
                value={contextWindowSize}
                onChange={(e) => setContextWindowSize(Number(e.target.value))}
                className="w-20 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
              />
            </div>

            <div>
              <label className="text-sm text-gray-400 block mb-1">
                Progress
              </label>
              <div className="text-sm font-semibold">{progress}</div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={prevContext}
              disabled={currentContextIndex === 0}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ← Prev
            </button>
            <button
              onClick={nextContext}
              disabled={currentContextIndex === contexts.length - 1}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
        </div>

        {/* Highlight Controls */}
        <div className="flex items-center gap-2 flex-wrap">
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={highlightInput}
              onChange={(e) => setHighlightInput(e.target.value)}
              placeholder="Characters to highlight..."
              className="px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm w-40"
            />
            <button
              onClick={handleAddHighlight}
              className="px-3 py-1 bg-blue-600 hover:bg-blue-500 rounded text-sm"
            >
              Add Highlight
            </button>
          </div>

          {contextHighlightChars.length > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-400">Highlighting:</span>
              {contextHighlightChars.map(char => (
                <span
                  key={char}
                  className="px-2 py-1 bg-blue-600 rounded text-sm chinese-char"
                >
                  {char}
                </span>
              ))}
              <button
                onClick={() => setContextHighlight([])}
                className="text-sm text-gray-400 hover:text-white"
              >
                Clear
              </button>
            </div>
          )}

          {contextHighlightChars.length >= 2 && (
            <button
              onClick={handleCreateContrast}
              className="px-3 py-1 bg-green-600 hover:bg-green-500 rounded text-sm ml-auto"
            >
              Create Contrast Hypothesis
            </button>
          )}
        </div>
      </div>

      {/* Context Display */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-4xl mx-auto">
          {/* Location */}
          <div className="mb-4 text-sm text-gray-400">
            Chapter {currentContext.chapter}, Position {currentContext.position}
          </div>

          {/* Context Window */}
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <div className="flex items-center justify-center flex-wrap leading-relaxed">
              {currentContext.before.map((char, i) => renderCharacter(char))}
              <span className="mx-2 text-yellow-400">[</span>
              {renderCharacter(currentContext.character, true)}
              <span className="mx-2 text-yellow-400">]</span>
              {currentContext.after.map((char, i) => renderCharacter(char))}
            </div>
          </div>

          {/* Character Info */}
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <h3 className="text-lg font-semibold mb-2">Character Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-3xl chinese-char">
                  {currentContext.character.char}
                </span>
              </div>
              <div>
                <div className="text-sm text-gray-400">Pinyin</div>
                <div>{currentContext.character.pinyin}</div>
              </div>
            </div>
          </div>

          {/* Add Annotation */}
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-sm font-semibold mb-2">Add Annotation</h3>
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Enter your observation about this context..."
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm mb-2"
              rows={3}
            />
            <div className="flex gap-2">
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="Tags (comma-separated)"
                className="flex-1 px-3 py-1 bg-gray-700 border border-gray-600 rounded text-sm"
              />
              <button
                onClick={handleAddAnnotation}
                disabled={!note.trim()}
                className="px-4 py-1 bg-blue-600 hover:bg-blue-500 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Add Note
              </button>
            </div>
          </div>

          {/* Quick Navigation */}
          <div className="mt-6">
            <h3 className="text-sm font-semibold mb-2">Jump to Instance</h3>
            <div className="flex gap-1 flex-wrap">
              {contexts.map((_, index) => (
                <button
                  key={index}
                  onClick={() => goToContext(index)}
                  className={`px-2 py-1 rounded text-xs ${
                    index === currentContextIndex
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 hover:bg-gray-600'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
