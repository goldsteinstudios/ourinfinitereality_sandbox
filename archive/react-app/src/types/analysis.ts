import type { Character, CharacterOccurrence } from './index';

// Co-occurrence Analysis Types
export interface CoOccurrencePair {
  char1: string;
  char2: string;
  count: number;
  instances: CoOccurrenceInstance[];
}

export interface CoOccurrenceInstance {
  char1Occurrence: CharacterOccurrence;
  char2Occurrence: CharacterOccurrence;
  proximity: number; // Distance between the two characters
  context: string; // Surrounding text snippet
}

export interface CoOccurrenceMatrix {
  characters: string[]; // Unique characters in the matrix
  matrix: Map<string, Map<string, CoOccurrencePair>>; // char1 -> char2 -> pair data
  proximityThreshold: number;
  minFrequency: number;
}

// Context Viewer Types
export interface ContextWindow {
  character: Character;
  before: Character[];
  after: Character[];
  windowSize: number;
  chapter: number;
  position: number;
}

export interface ContextAnnotation {
  id: string;
  characterOccurrence: CharacterOccurrence;
  note: string;
  timestamp: number;
  tags: string[];
}

// Contrast Pair Analysis Types
export type InstanceClassification = 'oppose' | 'align' | 'ambiguous' | 'independent';

export interface ContrastInstance {
  id: string;
  char1Occurrence: CharacterOccurrence;
  char2Occurrence: CharacterOccurrence;
  classification: InstanceClassification | null;
  context: ContextWindow;
  note: string;
  timestamp: number;
}

export interface ContrastHypothesis {
  id: string;
  char1: string;
  char2: string;
  name: string;
  description: string;
  instances: ContrastInstance[];
  statistics: ContrastStatistics;
  createdAt: number;
  updatedAt: number;
}

export interface ContrastStatistics {
  total: number;
  oppose: number;
  align: number;
  ambiguous: number;
  independent: number;
  unclassified: number;
  oppositionRate: number; // oppose / (total - unclassified)
  alignmentRate: number;
  confidenceLevel: 'low' | 'medium' | 'high' | 'very-high';
}

// Analysis Tool State Types
export type AnalysisTool = 'matrix' | 'context' | 'contrast';

export interface AnalysisFilters {
  chapterRange?: [number, number];
  minFrequency?: number;
  proximityThreshold?: number;
  searchQuery?: string;
}

// Export Types
export interface AnalysisReport {
  type: 'contrast-pair' | 'co-occurrence' | 'context';
  title: string;
  hypothesis?: ContrastHypothesis;
  matrix?: CoOccurrenceMatrix;
  contexts?: ContextWindow[];
  generatedAt: number;
  author?: string;
}

export type ExportFormat = 'csv' | 'json' | 'markdown' | 'pdf';
