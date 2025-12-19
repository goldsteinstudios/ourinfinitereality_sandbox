import React, { useState, useEffect } from 'react';
import { useMotionStore } from '../../store/useMotionStore';
import type { MotionDescription } from '../../types/motion';

export const MotionImagination: React.FC = () => {
  const { currentInsight, updateMotion } = useMotionStore();
  const [physicalAction, setPhysicalAction] = useState('');
  const [motion, setMotion] = useState<MotionDescription>({
    action: '',
    directionality: 'linear',
    force: 'smooth',
    spatialExtent: 'local',
    temporalAspect: 'momentary',
    energyFlow: '',
  });

  useEffect(() => {
    if (currentInsight) {
      setPhysicalAction(currentInsight.physicalAction);
      setMotion(currentInsight.motionDescription);
    }
  }, [currentInsight]);

  const handleSave = () => {
    updateMotion(motion, physicalAction);
  };

  if (!currentInsight) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-purple-900 mb-2">
              <span className="text-5xl font-serif mr-4">{currentInsight.character}</span>
              ({currentInsight.pinyin})
            </h2>
            <p className="text-sm text-purple-800">
              Imagine the physical motion this character encodes. What do you see? What do you
              feel?
            </p>
          </div>
        </div>
      </div>

      {/* Main Prompt: Imagine the Motion */}
      <div className="bg-white rounded-lg border-2 border-purple-300 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🎬 Imagine: What physical motion does this show?
        </h3>

        {currentInsight.tool && (
          <div className="mb-4 p-4 bg-blue-50 rounded-lg">
            <div className="text-sm text-blue-900">
              <strong>Tool identified:</strong> {currentInsight.tool.name} (
              {currentInsight.tool.category})
            </div>
            <div className="text-sm text-blue-800 mt-1">{currentInsight.tool.description}</div>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Close your eyes. Imagine using this {currentInsight.tool?.name || 'tool/action'}.
              Describe the motion you make:
            </label>
            <textarea
              value={physicalAction}
              onChange={(e) => setPhysicalAction(e.target.value)}
              onBlur={handleSave}
              placeholder="Example: 'I swing the scythe in a wide arc, starting high and bringing it down in a smooth circular motion. My body rotates slightly with each swing, creating a spiral pattern as I move forward through the grain...'"
              rows={6}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            />
            <div className="mt-2 text-xs text-gray-500">
              Be specific: What direction? What rhythm? What pattern does the motion trace in
              space?
            </div>
          </div>

          {/* Guided Questions */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-3">
            <div className="text-sm font-medium text-gray-700 mb-2">Guided Questions:</div>
            <div className="space-y-2 text-sm text-gray-600">
              <div>• How do you hold it?</div>
              <div>• What motion do you make?</div>
              <div>• Is it circular, linear, or something else?</div>
              <div>• Is it sharp and sudden, or smooth and flowing?</div>
              <div>• What pattern does it trace in space?</div>
              <div>• How does energy flow through the motion?</div>
            </div>
          </div>
        </div>
      </div>

      {/* Motion Characteristics */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-6">
        <h3 className="text-lg font-semibold text-gray-900">Motion Characteristics</h3>

        {/* Action Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Action Summary (one line)
          </label>
          <input
            type="text"
            value={motion.action}
            onChange={(e) => setMotion({ ...motion, action: e.target.value })}
            onBlur={handleSave}
            placeholder="e.g., 'swing in circular arc'"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
          />
        </div>

        {/* Directionality */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Directionality</label>
          <div className="grid grid-cols-4 gap-2">
            {(['linear', 'circular', 'radial', 'complex'] as const).map((dir) => (
              <button
                key={dir}
                onClick={() => {
                  setMotion({ ...motion, directionality: dir });
                  handleSave();
                }}
                className={`px-4 py-2 text-sm rounded-lg transition-colors ${
                  motion.directionality === dir
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {dir.charAt(0).toUpperCase() + dir.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Force Quality */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Force Quality</label>
          <div className="grid grid-cols-5 gap-2">
            {(['sharp', 'smooth', 'rhythmic', 'sustained', 'sudden'] as const).map((f) => (
              <button
                key={f}
                onClick={() => {
                  setMotion({ ...motion, force: f });
                  handleSave();
                }}
                className={`px-4 py-2 text-sm rounded-lg transition-colors ${
                  motion.force === f
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Spatial Extent */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Spatial Extent</label>
          <div className="grid grid-cols-3 gap-2">
            {(['local', 'expansive', 'contained'] as const).map((extent) => (
              <button
                key={extent}
                onClick={() => {
                  setMotion({ ...motion, spatialExtent: extent });
                  handleSave();
                }}
                className={`px-4 py-2 text-sm rounded-lg transition-colors ${
                  motion.spatialExtent === extent
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {extent.charAt(0).toUpperCase() + extent.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Temporal Aspect */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Temporal Aspect</label>
          <div className="grid grid-cols-4 gap-2">
            {(['momentary', 'repeated', 'continuous', 'cyclical'] as const).map((temp) => (
              <button
                key={temp}
                onClick={() => {
                  setMotion({ ...motion, temporalAspect: temp });
                  handleSave();
                }}
                className={`px-4 py-2 text-sm rounded-lg transition-colors ${
                  motion.temporalAspect === temp
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {temp.charAt(0).toUpperCase() + temp.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Energy Flow */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Energy Flow Description
          </label>
          <textarea
            value={motion.energyFlow}
            onChange={(e) => setMotion({ ...motion, energyFlow: e.target.value })}
            onBlur={handleSave}
            placeholder="Describe how energy moves through this motion..."
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 resize-none"
          />
        </div>
      </div>

      {/* Example for 利 */}
      {currentInsight.character === '利' && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="text-sm font-medium text-amber-900 mb-2">💡 Example for 利:</div>
          <div className="text-sm text-amber-800 space-y-1">
            <div>
              <strong>Action:</strong> Swing scythe in circular arc through grain field
            </div>
            <div>
              <strong>Directionality:</strong> Circular (with forward progression creating spiral)
            </div>
            <div>
              <strong>Force:</strong> Smooth, rhythmic
            </div>
            <div>
              <strong>Energy Flow:</strong> Energy builds in the backswing, releases smoothly
              through the cut, follows natural golden ratio proportions
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
