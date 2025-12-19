import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { MotionInsight, MotionDecoderState } from '../types/motion';

interface MotionStore extends MotionDecoderState {
  // Navigation
  setStep: (step: number) => void;
  nextStep: () => void;
  prevStep: () => void;
  resetWizard: () => void;

  // Working Insight Management
  updateWorkingInsight: (updates: Partial<MotionInsight>) => void;
  startNewInsight: (character: string) => void;
  saveInsight: () => void;
  discardInsight: () => void;

  // Saved Insights Management
  loadInsight: (id: string) => void;
  deleteInsight: (id: string) => void;
  exportInsight: (id: string) => string;
  importInsight: (jsonString: string) => void;

  // Comparison Mode
  toggleComparisonMode: () => void;
  toggleInsightComparison: (id: string) => void;
  clearComparison: () => void;
}

export const useMotionStore = create<MotionStore>()(
  persist(
    (set, get) => ({
      // Initial State
      currentStep: 1,
      workingInsight: null,
      savedInsights: [],
      comparisonMode: false,
      comparisonInsights: [],

      // Navigation
      setStep: (step: number) => {
        if (step >= 1 && step <= 8) {
          set({ currentStep: step });
        }
      },

      nextStep: () => {
        const { currentStep } = get();
        if (currentStep < 8) {
          set({ currentStep: currentStep + 1 });
        }
      },

      prevStep: () => {
        const { currentStep } = get();
        if (currentStep > 1) {
          set({ currentStep: currentStep - 1 });
        }
      },

      resetWizard: () => {
        set({ currentStep: 1, workingInsight: null });
      },

      // Working Insight Management
      updateWorkingInsight: (updates: Partial<MotionInsight>) => {
        set((state) => ({
          workingInsight: {
            ...state.workingInsight,
            ...updates,
          },
        }));
      },

      startNewInsight: (character: string) => {
        const id = `insight-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        set({
          currentStep: 1,
          workingInsight: {
            id,
            timestamp: Date.now(),
            character,
            radicals: [],
            tools: [],
            geometricPatterns: [],
            mathematicalRelationships: [],
            contextTests: [],
            tags: [],
          },
        });
      },

      saveInsight: () => {
        const { workingInsight, savedInsights } = get();
        if (workingInsight && workingInsight.character) {
          const completeInsight: MotionInsight = {
            id: workingInsight.id || `insight-${Date.now()}`,
            timestamp: workingInsight.timestamp || Date.now(),
            character: workingInsight.character,
            characterInfo: workingInsight.characterInfo || { pinyin: '', occurrences: [] },
            radicals: workingInsight.radicals || [],
            tools: workingInsight.tools || [],
            motion: workingInsight.motion || {
              action: '',
              directionality: '',
              force: '',
              spatialExtent: '',
              temporalAspect: '',
            },
            geometricPatterns: workingInsight.geometricPatterns || [],
            mathematicalRelationships: workingInsight.mathematicalRelationships || [],
            contextTests: workingInsight.contextTests || [],
            hypothesis: workingInsight.hypothesis || '',
            confidence: workingInsight.confidence || 'medium',
            notes: workingInsight.notes || '',
            tags: workingInsight.tags || [],
          };

          set({
            savedInsights: [...savedInsights, completeInsight],
            workingInsight: null,
            currentStep: 1,
          });
        }
      },

      discardInsight: () => {
        set({ workingInsight: null, currentStep: 1 });
      },

      // Saved Insights Management
      loadInsight: (id: string) => {
        const { savedInsights } = get();
        const insight = savedInsights.find((i) => i.id === id);
        if (insight) {
          set({
            workingInsight: { ...insight },
            currentStep: 1,
          });
        }
      },

      deleteInsight: (id: string) => {
        set((state) => ({
          savedInsights: state.savedInsights.filter((i) => i.id !== id),
          comparisonInsights: state.comparisonInsights.filter((cid) => cid !== id),
        }));
      },

      exportInsight: (id: string) => {
        const { savedInsights } = get();
        const insight = savedInsights.find((i) => i.id === id);
        return insight ? JSON.stringify(insight, null, 2) : '';
      },

      importInsight: (jsonString: string) => {
        try {
          const insight = JSON.parse(jsonString) as MotionInsight;
          set((state) => ({
            savedInsights: [...state.savedInsights, insight],
          }));
        } catch (error) {
          console.error('Failed to import insight:', error);
        }
      },

      // Comparison Mode
      toggleComparisonMode: () => {
        set((state) => ({
          comparisonMode: !state.comparisonMode,
          comparisonInsights: state.comparisonMode ? [] : state.comparisonInsights,
        }));
      },

      toggleInsightComparison: (id: string) => {
        set((state) => {
          const isSelected = state.comparisonInsights.includes(id);
          return {
            comparisonInsights: isSelected
              ? state.comparisonInsights.filter((cid) => cid !== id)
              : [...state.comparisonInsights, id],
          };
        });
      },

      clearComparison: () => {
        set({ comparisonInsights: [] });
      },
    }),
    {
      name: 'motion-decoder-storage',
      partialize: (state) => ({
        savedInsights: state.savedInsights,
      }),
    }
  )
);
