import { create } from 'zustand';
import type {
  AnalysisTool,
  CoOccurrenceMatrix,
  CoOccurrencePair,
  ContextWindow,
  ContrastHypothesis,
  ContrastInstance,
  InstanceClassification,
  ContextAnnotation,
} from '../types/analysis';
import { calculateCoOccurrenceMatrix, getCoOccurrencePair } from '../utils/coOccurrenceCalculator';
import { extractContextWindow, extractAllContexts } from '../utils/contextExtractor';
import { useAppStore } from './useAppStore';

interface AnalysisState {
  // Active tool
  activeTool: AnalysisTool;

  // Co-occurrence Matrix
  matrix: CoOccurrenceMatrix | null;
  matrixLoading: boolean;
  proximityThreshold: number;
  minFrequency: number;
  selectedPair: CoOccurrencePair | null;

  // Context Viewer
  contexts: ContextWindow[];
  currentContextIndex: number;
  contextWindowSize: number;
  contextAnnotations: ContextAnnotation[];
  contextHighlightChars: string[];

  // Contrast Pair Analyzer
  hypotheses: ContrastHypothesis[];
  activeHypothesis: ContrastHypothesis | null;
  currentInstanceIndex: number;

  // Actions - Tool Switching
  setActiveTool: (tool: AnalysisTool) => void;

  // Actions - Co-occurrence Matrix
  generateMatrix: () => void;
  setProximityThreshold: (threshold: number) => void;
  setMinFrequency: (frequency: number) => void;
  selectPair: (char1: string, char2: string) => void;
  clearPair: () => void;

  // Actions - Context Viewer
  viewCharacterContexts: (char: string) => void;
  setContextWindowSize: (size: number) => void;
  nextContext: () => void;
  prevContext: () => void;
  goToContext: (index: number) => void;
  addContextAnnotation: (note: string, tags: string[]) => void;
  setContextHighlight: (chars: string[]) => void;

  // Actions - Contrast Analyzer
  createHypothesis: (char1: string, char2: string, name: string, description: string) => void;
  selectHypothesis: (hypothesisId: string) => void;
  classifyInstance: (instanceId: string, classification: InstanceClassification) => void;
  addInstanceNote: (instanceId: string, note: string) => void;
  nextInstance: () => void;
  prevInstance: () => void;
  deleteHypothesis: (hypothesisId: string) => void;
  updateHypothesisStats: (hypothesisId: string) => void;

  // Integrated Workflows
  pairToContext: (char1: string, char2: string) => void;
  contextToContrast: (char1: string, char2: string) => void;
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  // Initial state
  activeTool: 'matrix',
  matrix: null,
  matrixLoading: false,
  proximityThreshold: 5,
  minFrequency: 2,
  selectedPair: null,
  contexts: [],
  currentContextIndex: 0,
  contextWindowSize: 5,
  contextAnnotations: [],
  contextHighlightChars: [],
  hypotheses: [],
  activeHypothesis: null,
  currentInstanceIndex: 0,

  // Tool Switching
  setActiveTool: (tool) => set({ activeTool: tool }),

  // Co-occurrence Matrix Actions
  generateMatrix: () => {
    set({ matrixLoading: true });

    const appData = useAppStore.getState().data;
    if (!appData) {
      set({ matrixLoading: false });
      return;
    }

    const { proximityThreshold, minFrequency } = get();
    const matrix = calculateCoOccurrenceMatrix(
      appData.characters,
      appData.characterMap,
      proximityThreshold,
      minFrequency
    );

    set({ matrix, matrixLoading: false });
  },

  setProximityThreshold: (threshold) => {
    set({ proximityThreshold: threshold });
    // Regenerate matrix with new threshold
    get().generateMatrix();
  },

  setMinFrequency: (frequency) => {
    set({ minFrequency: frequency });
    // Regenerate matrix with new threshold
    get().generateMatrix();
  },

  selectPair: (char1, char2) => {
    const { matrix } = get();
    if (!matrix) return;

    const pair = getCoOccurrencePair(matrix, char1, char2);
    set({ selectedPair: pair });
  },

  clearPair: () => set({ selectedPair: null }),

  // Context Viewer Actions
  viewCharacterContexts: (char) => {
    const appData = useAppStore.getState().data;
    if (!appData) return;

    const { contextWindowSize } = get();
    const contexts = extractAllContexts(appData, char, contextWindowSize);
    set({ contexts, currentContextIndex: 0, contextHighlightChars: [char] });
  },

  setContextWindowSize: (size) => {
    set({ contextWindowSize: size });
    // Refresh contexts with new window size
    const { contexts } = get();
    if (contexts.length > 0) {
      const char = contexts[0].character.char;
      get().viewCharacterContexts(char);
    }
  },

  nextContext: () => {
    const { contexts, currentContextIndex } = get();
    if (currentContextIndex < contexts.length - 1) {
      set({ currentContextIndex: currentContextIndex + 1 });
    }
  },

  prevContext: () => {
    const { currentContextIndex } = get();
    if (currentContextIndex > 0) {
      set({ currentContextIndex: currentContextIndex - 1 });
    }
  },

  goToContext: (index) => {
    const { contexts } = get();
    if (index >= 0 && index < contexts.length) {
      set({ currentContextIndex: index });
    }
  },

  addContextAnnotation: (note, tags) => {
    const { contexts, currentContextIndex, contextAnnotations } = get();
    const context = contexts[currentContextIndex];
    if (!context) return;

    const annotation: ContextAnnotation = {
      id: `${Date.now()}_${Math.random()}`,
      characterOccurrence: {
        chapter: context.chapter,
        position: context.position,
      },
      note,
      tags,
      timestamp: Date.now(),
    };

    set({ contextAnnotations: [...contextAnnotations, annotation] });
  },

  setContextHighlight: (chars) => {
    set({ contextHighlightChars: chars });
  },

  // Contrast Analyzer Actions
  createHypothesis: (char1, char2, name, description) => {
    const appData = useAppStore.getState().data;
    const { matrix } = get();
    if (!appData || !matrix) return;

    const pair = getCoOccurrencePair(matrix, char1, char2);
    if (!pair) return;

    // Create contrast instances from co-occurrence instances
    const instances: ContrastInstance[] = pair.instances.map(instance => {
      const context = extractContextWindow(
        appData,
        instance.char1Occurrence,
        5
      );

      return {
        id: `${Date.now()}_${Math.random()}`,
        char1Occurrence: instance.char1Occurrence,
        char2Occurrence: instance.char2Occurrence,
        classification: null,
        context: context!,
        note: '',
        timestamp: Date.now(),
      };
    });

    const hypothesis: ContrastHypothesis = {
      id: `hyp_${Date.now()}`,
      char1,
      char2,
      name,
      description,
      instances,
      statistics: {
        total: instances.length,
        oppose: 0,
        align: 0,
        ambiguous: 0,
        independent: 0,
        unclassified: instances.length,
        oppositionRate: 0,
        alignmentRate: 0,
        confidenceLevel: 'low',
      },
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };

    set({
      hypotheses: [...get().hypotheses, hypothesis],
      activeHypothesis: hypothesis,
      currentInstanceIndex: 0,
      activeTool: 'contrast',
    });
  },

  selectHypothesis: (hypothesisId) => {
    const hypothesis = get().hypotheses.find(h => h.id === hypothesisId);
    if (hypothesis) {
      set({ activeHypothesis: hypothesis, currentInstanceIndex: 0 });
    }
  },

  classifyInstance: (instanceId, classification) => {
    const { activeHypothesis } = get();
    if (!activeHypothesis) return;

    const updatedInstances = activeHypothesis.instances.map(instance =>
      instance.id === instanceId
        ? { ...instance, classification, timestamp: Date.now() }
        : instance
    );

    const updatedHypothesis = {
      ...activeHypothesis,
      instances: updatedInstances,
      updatedAt: Date.now(),
    };

    // Update statistics
    get().updateHypothesisStats(updatedHypothesis.id);

    set({
      activeHypothesis: updatedHypothesis,
      hypotheses: get().hypotheses.map(h =>
        h.id === activeHypothesis.id ? updatedHypothesis : h
      ),
    });
  },

  addInstanceNote: (instanceId, note) => {
    const { activeHypothesis } = get();
    if (!activeHypothesis) return;

    const updatedInstances = activeHypothesis.instances.map(instance =>
      instance.id === instanceId
        ? { ...instance, note, timestamp: Date.now() }
        : instance
    );

    const updatedHypothesis = {
      ...activeHypothesis,
      instances: updatedInstances,
      updatedAt: Date.now(),
    };

    set({
      activeHypothesis: updatedHypothesis,
      hypotheses: get().hypotheses.map(h =>
        h.id === activeHypothesis.id ? updatedHypothesis : h
      ),
    });
  },

  nextInstance: () => {
    const { activeHypothesis, currentInstanceIndex } = get();
    if (!activeHypothesis) return;

    if (currentInstanceIndex < activeHypothesis.instances.length - 1) {
      set({ currentInstanceIndex: currentInstanceIndex + 1 });
    }
  },

  prevInstance: () => {
    const { currentInstanceIndex } = get();
    if (currentInstanceIndex > 0) {
      set({ currentInstanceIndex: currentInstanceIndex - 1 });
    }
  },

  deleteHypothesis: (hypothesisId) => {
    const { hypotheses, activeHypothesis } = get();
    set({
      hypotheses: hypotheses.filter(h => h.id !== hypothesisId),
      activeHypothesis: activeHypothesis?.id === hypothesisId ? null : activeHypothesis,
    });
  },

  updateHypothesisStats: (hypothesisId) => {
    const hypothesis = get().hypotheses.find(h => h.id === hypothesisId);
    if (!hypothesis) return;

    const instances = hypothesis.instances;
    const total = instances.length;
    const oppose = instances.filter(i => i.classification === 'oppose').length;
    const align = instances.filter(i => i.classification === 'align').length;
    const ambiguous = instances.filter(i => i.classification === 'ambiguous').length;
    const independent = instances.filter(i => i.classification === 'independent').length;
    const unclassified = instances.filter(i => i.classification === null).length;

    const classified = total - unclassified;
    const oppositionRate = classified > 0 ? oppose / classified : 0;
    const alignmentRate = classified > 0 ? align / classified : 0;

    // Determine confidence level
    let confidenceLevel: 'low' | 'medium' | 'high' | 'very-high' = 'low';
    if (classified >= 30) {
      if (oppositionRate > 0.8 || alignmentRate > 0.8) {
        confidenceLevel = 'very-high';
      } else if (oppositionRate > 0.6 || alignmentRate > 0.6) {
        confidenceLevel = 'high';
      } else {
        confidenceLevel = 'medium';
      }
    } else if (classified >= 15) {
      if (oppositionRate > 0.7 || alignmentRate > 0.7) {
        confidenceLevel = 'high';
      } else {
        confidenceLevel = 'medium';
      }
    }

    const updatedHypothesis = {
      ...hypothesis,
      statistics: {
        total,
        oppose,
        align,
        ambiguous,
        independent,
        unclassified,
        oppositionRate,
        alignmentRate,
        confidenceLevel,
      },
      updatedAt: Date.now(),
    };

    set({
      hypotheses: get().hypotheses.map(h =>
        h.id === hypothesisId ? updatedHypothesis : h
      ),
      activeHypothesis: get().activeHypothesis?.id === hypothesisId
        ? updatedHypothesis
        : get().activeHypothesis,
    });
  },

  // Integrated Workflows
  pairToContext: (char1, char2) => {
    // Select the pair in matrix, then switch to context view showing one of the characters
    get().selectPair(char1, char2);
    get().viewCharacterContexts(char1);
    set({ activeTool: 'context', contextHighlightChars: [char1, char2] });
  },

  contextToContrast: (char1, char2) => {
    // Generate a hypothesis from the current context view
    const name = `${char1}/${char2} Contrast Analysis`;
    const description = `Systematic analysis of opposition pattern between ${char1} and ${char2}`;
    get().createHypothesis(char1, char2, name, description);
  },
}));
