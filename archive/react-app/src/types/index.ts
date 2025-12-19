export interface Character {
  char: string;
  pinyin: string;
  chapter: number;
  position: number; // Row number in the text
  radicals?: string[];
  operatorType?: 'O' | 'G' | 'P' | 'frame' | 'perception';
  notes?: string[];
}

export interface CharacterOccurrence {
  chapter: number;
  position: number;
}

export interface CharacterData {
  character: string;
  pinyin: string;
  occurrences: CharacterOccurrence[];
}

export interface Hypothesis {
  id: string;
  name: string;
  description: string;
  charactersToTest: string[];
  results: {
    [characterKey: string]: {
      status: 'support' | 'contradict' | 'ambiguous';
      note: string;
    }
  };
  statistics: {
    support: number;
    contradict: number;
    ambiguous: number;
  };
}

export interface RadicalInfo {
  radical: string;
  name: string;
  color: string;
}

export type HighlightMode = 'union' | 'intersection';
