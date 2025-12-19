import { create } from 'zustand';
import type { Character, CharacterData, ParsedCSVData, HighlightMode } from '../types';

interface AppState {
  // Data
  data: ParsedCSVData | null;
  isLoading: boolean;
  error: string | null;

  // Character detail panel
  selectedCharacter: Character | null;
  selectedCharacterData: CharacterData | null;

  // Highlighting
  selectedRadicals: string[];
  highlightMode: HighlightMode;

  // Search
  searchQuery: string;
  searchResults: Character[];

  // Actions
  setData: (data: ParsedCSVData) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  selectCharacter: (character: Character | null) => void;
  toggleRadical: (radical: string) => void;
  clearRadicals: () => void;
  setHighlightMode: (mode: HighlightMode) => void;
  setSearchQuery: (query: string) => void;
  performSearch: (query: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  data: null,
  isLoading: false,
  error: null,
  selectedCharacter: null,
  selectedCharacterData: null,
  selectedRadicals: [],
  highlightMode: 'union',
  searchQuery: '',
  searchResults: [],

  // Actions
  setData: (data) => set({ data, isLoading: false, error: null }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error, isLoading: false }),

  selectCharacter: (character) => {
    const { data } = get();
    if (!character || !data) {
      set({ selectedCharacter: null, selectedCharacterData: null });
      return;
    }

    const characterData = data.characterMap.get(character.char);
    set({
      selectedCharacter: character,
      selectedCharacterData: characterData || null
    });
  },

  toggleRadical: (radical) => {
    const { selectedRadicals } = get();
    const newRadicals = selectedRadicals.includes(radical)
      ? selectedRadicals.filter(r => r !== radical)
      : [...selectedRadicals, radical];
    set({ selectedRadicals: newRadicals });
  },

  clearRadicals: () => set({ selectedRadicals: [] }),

  setHighlightMode: (mode) => set({ highlightMode: mode }),

  setSearchQuery: (query) => set({ searchQuery: query }),

  performSearch: (query) => {
    const { data } = get();
    if (!data || !query) {
      set({ searchResults: [], searchQuery: query });
      return;
    }

    const results = data.characters.filter(char =>
      char.char === query || char.pinyin.toLowerCase().includes(query.toLowerCase())
    );

    set({ searchResults: results, searchQuery: query });
  },
}));
