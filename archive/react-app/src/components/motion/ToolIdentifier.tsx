import React, { useState, useEffect } from 'react';
import { useMotionStore } from '../../store/useMotionStore';
import type { ToolCategory, ToolIdentification } from '../../types/motion';

const TOOL_CATEGORIES: { value: ToolCategory; label: string; examples: string }[] = [
  { value: 'blade', label: 'Blade', examples: 'knives, scythes, swords' },
  { value: 'agriculture', label: 'Agriculture', examples: 'plows, hoes, rakes' },
  { value: 'construction', label: 'Construction', examples: 'hammers, axes, saws' },
  { value: 'writing', label: 'Writing', examples: 'brushes, styluses' },
  { value: 'weaving', label: 'Weaving', examples: 'looms, shuttles' },
  { value: 'container', label: 'Container', examples: 'vessels, baskets, jars' },
  { value: 'weapon', label: 'Weapon', examples: 'spears, bows, shields' },
  { value: 'body', label: 'Body', examples: 'hand, foot, mouth, eye' },
  { value: 'natural', label: 'Natural', examples: 'water, fire, wind' },
  { value: 'abstract', label: 'Abstract', examples: 'concepts, relations' },
];

export const ToolIdentifier: React.FC = () => {
  const { currentInsight, updateTool } = useMotionStore();
  const [hasTool, setHasTool] = useState(false);
  const [tool, setTool] = useState<ToolIdentification>({
    name: '',
    category: 'abstract',
    description: '',
    radicals: [],
    gripDescription: '',
    confidence: 0.5,
  });

  useEffect(() => {
    if (currentInsight?.tool) {
      setHasTool(true);
      setTool(currentInsight.tool);
    }
  }, [currentInsight]);

  const handleSave = () => {
    updateTool(hasTool ? tool : undefined);
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-green-900 mb-2">
          <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
          Tool Identification
        </h2>
        <p className="text-sm text-green-800">
          Does this character depict a physical tool or implement? If so, identify it.
        </p>
      </div>

      {/* Has Tool? */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <label className="block text-sm font-medium text-gray-700 mb-4">
          Does this character contain or represent a tool?
        </label>
        <div className="flex space-x-4">
          <button
            onClick={() => {
              setHasTool(true);
              handleSave();
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              hasTool
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Yes, contains a tool
          </button>
          <button
            onClick={() => {
              setHasTool(false);
              handleSave();
            }}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              !hasTool
                ? 'bg-gray-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            No tool (abstract concept)
          </button>
        </div>
      </div>

      {hasTool && (
        <>
          {/* Tool Details */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">Tool Details</h3>

            {/* Tool Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                What tool is this?
              </label>
              <input
                type="text"
                value={tool.name}
                onChange={(e) => setTool({ ...tool, name: e.target.value })}
                onBlur={handleSave}
                placeholder="e.g., 'scythe', 'hand', 'plow'"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              />
            </div>

            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tool Category
              </label>
              <div className="grid grid-cols-2 gap-3">
                {TOOL_CATEGORIES.map((cat) => (
                  <button
                    key={cat.value}
                    onClick={() => {
                      setTool({ ...tool, category: cat.value });
                      handleSave();
                    }}
                    className={`p-3 text-left rounded-lg border transition-colors ${
                      tool.category === cat.value
                        ? 'bg-green-100 border-green-500 text-green-900'
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                    }`}
                  >
                    <div className="font-medium">{cat.label}</div>
                    <div className="text-xs text-gray-600">{cat.examples}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                How is this tool used?
              </label>
              <textarea
                value={tool.description}
                onChange={(e) => setTool({ ...tool, description: e.target.value })}
                onBlur={handleSave}
                placeholder="Describe how this tool is used and what it does..."
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 resize-none"
              />
            </div>

            {/* Grip Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                How do you hold it? (optional)
              </label>
              <input
                type="text"
                value={tool.gripDescription || ''}
                onChange={(e) => setTool({ ...tool, gripDescription: e.target.value })}
                onBlur={handleSave}
                placeholder="e.g., 'two-handed grip', 'held at the base'"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              />
            </div>

            {/* Which Radicals */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Which radicals indicate this tool?
              </label>
              <div className="flex flex-wrap gap-2 mb-2">
                {currentInsight.radicals.map((radical) => (
                  <button
                    key={radical}
                    onClick={() => {
                      const newRadicals = tool.radicals.includes(radical)
                        ? tool.radicals.filter((r) => r !== radical)
                        : [...tool.radicals, radical];
                      setTool({ ...tool, radicals: newRadicals });
                      handleSave();
                    }}
                    className={`px-3 py-2 rounded-lg text-lg font-serif transition-colors ${
                      tool.radicals.includes(radical)
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {radical}
                  </button>
                ))}
              </div>
              <div className="text-xs text-gray-500">
                Select the radicals that specifically represent this tool
              </div>
            </div>

            {/* Confidence */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confidence: {Math.round(tool.confidence * 100)}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={tool.confidence * 100}
                onChange={(e) =>
                  setTool({ ...tool, confidence: parseInt(e.target.value) / 100 })
                }
                onMouseUp={handleSave}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Unsure</span>
                <span>Very Confident</span>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Example for 利 */}
      {currentInsight.character === '利' && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="text-sm font-medium text-amber-900 mb-2">💡 Example for 利:</div>
          <div className="text-sm text-amber-800 space-y-1">
            <div>
              <strong>Tool:</strong> Scythe
            </div>
            <div>
              <strong>Category:</strong> Blade (Agriculture)
            </div>
            <div>
              <strong>Description:</strong> A curved blade on a long handle for cutting grain in
              sweeping motions
            </div>
            <div>
              <strong>Grip:</strong> Two-handed, one hand on handle, one guiding the blade
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
