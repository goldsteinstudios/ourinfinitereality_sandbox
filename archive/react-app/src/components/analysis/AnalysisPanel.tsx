import { useAnalysisStore } from '../../store/useAnalysisStore';
import { CoOccurrenceMatrix } from './CoOccurrenceMatrix';
import { ContextViewer } from './ContextViewer';
import { ContrastAnalyzer } from './ContrastAnalyzer';
import type { AnalysisTool } from '../../types/analysis';

export function AnalysisPanel() {
  const { activeTool, setActiveTool } = useAnalysisStore();

  const tabs: { id: AnalysisTool; label: string; description: string }[] = [
    {
      id: 'matrix',
      label: 'Co-occurrence Matrix',
      description: 'Discover character pairs and relationships',
    },
    {
      id: 'context',
      label: 'Context Viewer',
      description: 'Examine character usage patterns',
    },
    {
      id: 'contrast',
      label: 'Contrast Analyzer',
      description: 'Test opposition hypotheses systematically',
    },
  ];

  return (
    <div className="h-full flex flex-col bg-gray-900">
      {/* Tab Navigation */}
      <div className="border-b border-gray-700 bg-gray-800">
        <div className="flex">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTool(tab.id)}
              className={`px-6 py-4 border-b-2 transition-colors ${
                activeTool === tab.id
                  ? 'border-blue-500 bg-gray-900 text-white'
                  : 'border-transparent text-gray-400 hover:text-white hover:bg-gray-750'
              }`}
            >
              <div className="font-semibold">{tab.label}</div>
              <div className="text-xs mt-1 opacity-75">{tab.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Tool Content */}
      <div className="flex-1 overflow-hidden">
        {activeTool === 'matrix' && <CoOccurrenceMatrix />}
        {activeTool === 'context' && <ContextViewer />}
        {activeTool === 'contrast' && <ContrastAnalyzer />}
      </div>
    </div>
  );
}
