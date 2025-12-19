import { useState } from 'react';
import { useAnalysisStore } from '../../store/useAnalysisStore';
import type { InstanceClassification } from '../../types/analysis';
import { exportContrastHypothesis } from '../../utils/reportGenerator';
import { formatContextWindow } from '../../utils/contextExtractor';

export function ContrastAnalyzer() {
  const {
    hypotheses,
    activeHypothesis,
    currentInstanceIndex,
    selectHypothesis,
    classifyInstance,
    addInstanceNote,
    nextInstance,
    prevInstance,
    deleteHypothesis,
  } = useAnalysisStore();

  const [showHypothesisList, setShowHypothesisList] = useState(hypotheses.length > 0 && !activeHypothesis);
  const [instanceNote, setInstanceNote] = useState('');

  if (showHypothesisList || (!activeHypothesis && hypotheses.length > 0)) {
    return <HypothesisList hypotheses={hypotheses} onSelect={(id) => {
      selectHypothesis(id);
      setShowHypothesisList(false);
    }} onDelete={deleteHypothesis} />;
  }

  if (!activeHypothesis) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <p className="text-gray-400 text-lg mb-4">No hypothesis loaded</p>
          <p className="text-gray-500 text-sm mb-4">
            Create a hypothesis from the Context Viewer by highlighting two characters
          </p>
          {hypotheses.length > 0 && (
            <button
              onClick={() => setShowHypothesisList(true)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded"
            >
              View Saved Hypotheses ({hypotheses.length})
            </button>
          )}
        </div>
      </div>
    );
  }

  const currentInstance = activeHypothesis.instances[currentInstanceIndex];
  const stats = activeHypothesis.statistics;
  const progress = `${currentInstanceIndex + 1} / ${activeHypothesis.instances.length}`;

  const handleClassify = (classification: InstanceClassification) => {
    classifyInstance(currentInstance.id, classification);
    // Auto-advance to next unclassified instance
    const nextUnclassified = activeHypothesis.instances.findIndex(
      (inst, idx) => idx > currentInstanceIndex && inst.classification === null
    );
    if (nextUnclassified !== -1 && currentInstanceIndex < activeHypothesis.instances.length - 1) {
      setTimeout(() => nextInstance(), 200);
    }
  };

  const handleAddNote = () => {
    if (instanceNote.trim()) {
      addInstanceNote(currentInstance.id, instanceNote);
      setInstanceNote('');
    }
  };

  const handleExport = (format: 'markdown' | 'csv' | 'pdf' | 'json') => {
    exportContrastHypothesis(activeHypothesis, format);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center justify-between mb-2">
          <div>
            <h2 className="text-xl font-bold">
              <span className="chinese-char text-2xl">{activeHypothesis.char1}</span>
              <span className="mx-2">/</span>
              <span className="chinese-char text-2xl">{activeHypothesis.char2}</span>
            </h2>
            <p className="text-sm text-gray-400">{activeHypothesis.name}</p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => setShowHypothesisList(true)}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
            >
              All Hypotheses
            </button>
            <div className="relative group">
              <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm">
                Export ▼
              </button>
              <div className="absolute right-0 mt-1 w-32 bg-gray-700 rounded shadow-lg hidden group-hover:block z-10">
                <button
                  onClick={() => handleExport('markdown')}
                  className="block w-full text-left px-3 py-2 hover:bg-gray-600 text-sm"
                >
                  Markdown
                </button>
                <button
                  onClick={() => handleExport('csv')}
                  className="block w-full text-left px-3 py-2 hover:bg-gray-600 text-sm"
                >
                  CSV
                </button>
                <button
                  onClick={() => handleExport('pdf')}
                  className="block w-full text-left px-3 py-2 hover:bg-gray-600 text-sm"
                >
                  PDF
                </button>
                <button
                  onClick={() => handleExport('json')}
                  className="block w-full text-left px-3 py-2 hover:bg-gray-600 text-sm"
                >
                  JSON
                </button>
              </div>
            </div>
          </div>
        </div>

        <p className="text-sm text-gray-400">{activeHypothesis.description}</p>
      </div>

      {/* Statistics */}
      <div className="p-4 bg-gray-750 border-b border-gray-700">
        <div className="grid grid-cols-5 gap-4 text-center">
          <StatBox label="Total" value={stats.total} color="bg-gray-600" />
          <StatBox label="Oppose" value={stats.oppose} color="bg-red-600" percentage={(stats.oppositionRate * 100).toFixed(1)} />
          <StatBox label="Align" value={stats.align} color="bg-green-600" percentage={(stats.alignmentRate * 100).toFixed(1)} />
          <StatBox label="Ambiguous" value={stats.ambiguous} color="bg-yellow-600" />
          <StatBox label="Unclassified" value={stats.unclassified} color="bg-gray-500" />
        </div>
        <div className="mt-3 text-center">
          <span className={`px-3 py-1 rounded text-sm font-semibold ${
            stats.confidenceLevel === 'very-high' ? 'bg-green-600' :
            stats.confidenceLevel === 'high' ? 'bg-blue-600' :
            stats.confidenceLevel === 'medium' ? 'bg-yellow-600' :
            'bg-gray-600'
          }`}>
            Confidence: {stats.confidenceLevel.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Navigation */}
      <div className="p-4 bg-gray-800 border-b border-gray-700 flex items-center justify-between">
        <button
          onClick={prevInstance}
          disabled={currentInstanceIndex === 0}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Previous
        </button>

        <div className="text-center">
          <div className="text-sm text-gray-400">Instance</div>
          <div className="text-lg font-semibold">{progress}</div>
        </div>

        <button
          onClick={nextInstance}
          disabled={currentInstanceIndex === activeHypothesis.instances.length - 1}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next →
        </button>
      </div>

      {/* Instance Display */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-4xl mx-auto">
          {/* Context */}
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <div className="text-sm text-gray-400 mb-4">
              {formatContextWindow(currentInstance.context, {
                showChapter: true,
                showPosition: true,
              })}
            </div>
            <div className="text-2xl chinese-char leading-relaxed text-center">
              {formatContextWindow(currentInstance.context, {
                highlightCenter: true,
              })}
            </div>
          </div>

          {/* Classification */}
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Classify this instance</h3>
            <div className="grid grid-cols-2 gap-3">
              <ClassificationButton
                label="Oppose"
                description="Characters function as opposites"
                color="bg-red-600 hover:bg-red-500"
                isSelected={currentInstance.classification === 'oppose'}
                onClick={() => handleClassify('oppose')}
              />
              <ClassificationButton
                label="Align"
                description="Characters support each other"
                color="bg-green-600 hover:bg-green-500"
                isSelected={currentInstance.classification === 'align'}
                onClick={() => handleClassify('align')}
              />
              <ClassificationButton
                label="Ambiguous"
                description="Relationship is unclear"
                color="bg-yellow-600 hover:bg-yellow-500"
                isSelected={currentInstance.classification === 'ambiguous'}
                onClick={() => handleClassify('ambiguous')}
              />
              <ClassificationButton
                label="Independent"
                description="Characters are unrelated"
                color="bg-gray-600 hover:bg-gray-500"
                isSelected={currentInstance.classification === 'independent'}
                onClick={() => handleClassify('independent')}
              />
            </div>
          </div>

          {/* Notes */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Notes</h3>
            {currentInstance.note && (
              <div className="mb-4 p-3 bg-gray-700 rounded">
                <p className="text-sm">{currentInstance.note}</p>
              </div>
            )}
            <textarea
              value={instanceNote}
              onChange={(e) => setInstanceNote(e.target.value)}
              placeholder="Add observations about this instance..."
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-sm mb-2"
              rows={3}
            />
            <button
              onClick={handleAddNote}
              disabled={!instanceNote.trim()}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm disabled:opacity-50"
            >
              {currentInstance.note ? 'Update Note' : 'Add Note'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Sub-components

function StatBox({ label, value, color, percentage }: {
  label: string;
  value: number;
  color: string;
  percentage?: string;
}) {
  return (
    <div className={`${color} rounded-lg p-3`}>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-xs text-gray-200">{label}</div>
      {percentage && <div className="text-sm font-semibold">{percentage}%</div>}
    </div>
  );
}

function ClassificationButton({ label, description, color, isSelected, onClick }: {
  label: string;
  description: string;
  color: string;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`p-4 rounded-lg transition-all ${color} ${
        isSelected ? 'ring-4 ring-blue-400' : ''
      }`}
    >
      <div className="font-semibold mb-1">{label}</div>
      <div className="text-xs opacity-90">{description}</div>
    </button>
  );
}

function HypothesisList({ hypotheses, onSelect, onDelete }: {
  hypotheses: any[];
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}) {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Saved Hypotheses</h2>
      <div className="grid gap-4">
        {hypotheses.map((hyp) => (
          <div key={hyp.id} className="bg-gray-800 rounded-lg p-4 flex items-center justify-between">
            <div className="flex-1 cursor-pointer" onClick={() => onSelect(hyp.id)}>
              <div className="font-semibold mb-1">
                <span className="chinese-char text-xl">{hyp.char1}</span>
                <span className="mx-2">/</span>
                <span className="chinese-char text-xl">{hyp.char2}</span>
                <span className="ml-3 text-sm text-gray-400">{hyp.name}</span>
              </div>
              <div className="text-sm text-gray-400">{hyp.description}</div>
              <div className="mt-2 flex gap-4 text-xs">
                <span>Total: {hyp.statistics.total}</span>
                <span>Oppose: {hyp.statistics.oppose}</span>
                <span>Align: {hyp.statistics.align}</span>
                <span className={`font-semibold ${
                  hyp.statistics.confidenceLevel === 'very-high' || hyp.statistics.confidenceLevel === 'high'
                    ? 'text-green-400'
                    : 'text-yellow-400'
                }`}>
                  {hyp.statistics.confidenceLevel}
                </span>
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (confirm('Delete this hypothesis?')) {
                  onDelete(hyp.id);
                }
              }}
              className="ml-4 px-3 py-1 bg-red-600 hover:bg-red-500 rounded text-sm"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
