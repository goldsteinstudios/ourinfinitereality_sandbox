import type { Character, CharacterData } from '../types';
import type {
  CoOccurrencePair,
  CoOccurrenceInstance,
  CoOccurrenceMatrix,
} from '../types/analysis';

/**
 * Calculate co-occurrence matrix for all characters in the text
 * Finds pairs of characters that appear within proximityThreshold of each other
 */
export function calculateCoOccurrenceMatrix(
  characters: Character[],
  characterMap: Map<string, CharacterData>,
  proximityThreshold: number = 5,
  minFrequency: number = 1
): CoOccurrenceMatrix {
  // Map to store co-occurrence pairs: char1 -> char2 -> pair data
  const pairMap = new Map<string, Map<string, CoOccurrencePair>>();
  const uniqueChars = new Set<string>();

  // Sort characters by chapter and position for efficient proximity search
  const sortedChars = [...characters].sort((a, b) => {
    if (a.chapter !== b.chapter) return a.chapter - b.chapter;
    return a.position - b.position;
  });

  // For each character, look ahead within proximity threshold
  for (let i = 0; i < sortedChars.length; i++) {
    const char1 = sortedChars[i];

    // Look ahead for potential pairs
    for (let j = i + 1; j < sortedChars.length; j++) {
      const char2 = sortedChars[j];

      // Stop if we've moved too far away
      if (char2.chapter !== char1.chapter) break;

      const distance = char2.position - char1.position;
      if (distance > proximityThreshold) break;

      // Don't count same character as co-occurrence with itself
      if (char1.char === char2.char) continue;

      // Record this co-occurrence
      recordCoOccurrence(
        pairMap,
        uniqueChars,
        char1,
        char2,
        distance,
        sortedChars,
        i,
        j
      );
    }
  }

  // Filter by minimum frequency
  const filteredMatrix = filterByFrequency(pairMap, minFrequency);

  return {
    characters: Array.from(uniqueChars).sort(),
    matrix: filteredMatrix,
    proximityThreshold,
    minFrequency,
  };
}

/**
 * Record a co-occurrence between two characters
 */
function recordCoOccurrence(
  pairMap: Map<string, Map<string, CoOccurrencePair>>,
  uniqueChars: Set<string>,
  char1: Character,
  char2: Character,
  distance: number,
  allChars: Character[],
  index1: number,
  index2: number
) {
  // Ensure char1 is lexicographically before char2 for consistent ordering
  const [c1, c2, i1, i2] =
    char1.char < char2.char
      ? [char1, char2, index1, index2]
      : [char2, char1, index2, index1];

  uniqueChars.add(c1.char);
  uniqueChars.add(c2.char);

  // Get or create the inner map for char1
  if (!pairMap.has(c1.char)) {
    pairMap.set(c1.char, new Map());
  }
  const innerMap = pairMap.get(c1.char)!;

  // Get or create the pair
  if (!innerMap.has(c2.char)) {
    innerMap.set(c2.char, {
      char1: c1.char,
      char2: c2.char,
      count: 0,
      instances: [],
    });
  }
  const pair = innerMap.get(c2.char)!;

  // Extract context window
  const context = extractContextForPair(allChars, i1, i2, 10);

  // Add this instance
  pair.instances.push({
    char1Occurrence: { chapter: c1.chapter, position: c1.position },
    char2Occurrence: { chapter: c2.chapter, position: c2.position },
    proximity: distance,
    context,
  });
  pair.count++;
}

/**
 * Extract context text around a pair of characters
 */
function extractContextForPair(
  allChars: Character[],
  index1: number,
  index2: number,
  windowSize: number
): string {
  const startIndex = Math.max(0, index1 - windowSize);
  const endIndex = Math.min(allChars.length - 1, index2 + windowSize);

  const contextChars = allChars.slice(startIndex, endIndex + 1);
  return contextChars.map(c => c.char).join('');
}

/**
 * Filter pairs by minimum frequency
 */
function filterByFrequency(
  pairMap: Map<string, Map<string, CoOccurrencePair>>,
  minFrequency: number
): Map<string, Map<string, CoOccurrencePair>> {
  const filtered = new Map<string, Map<string, CoOccurrencePair>>();

  for (const [char1, innerMap] of pairMap.entries()) {
    const filteredInner = new Map<string, CoOccurrencePair>();

    for (const [char2, pair] of innerMap.entries()) {
      if (pair.count >= minFrequency) {
        filteredInner.set(char2, pair);
      }
    }

    if (filteredInner.size > 0) {
      filtered.set(char1, filteredInner);
    }
  }

  return filtered;
}

/**
 * Get co-occurrence pair for two specific characters
 */
export function getCoOccurrencePair(
  matrix: CoOccurrenceMatrix,
  char1: string,
  char2: string
): CoOccurrencePair | null {
  // Ensure lexicographic order
  const [c1, c2] = char1 < char2 ? [char1, char2] : [char2, char1];

  const innerMap = matrix.matrix.get(c1);
  if (!innerMap) return null;

  return innerMap.get(c2) || null;
}

/**
 * Get all co-occurring characters for a given character
 */
export function getCoOccurringCharacters(
  matrix: CoOccurrenceMatrix,
  character: string
): CoOccurrencePair[] {
  const pairs: CoOccurrencePair[] = [];

  // Check as first character
  const innerMap = matrix.matrix.get(character);
  if (innerMap) {
    pairs.push(...Array.from(innerMap.values()));
  }

  // Check as second character
  for (const [char1, innerMap] of matrix.matrix.entries()) {
    if (char1 !== character && innerMap.has(character)) {
      pairs.push(innerMap.get(character)!);
    }
  }

  return pairs.sort((a, b) => b.count - a.count);
}

/**
 * Get top N most frequent pairs
 */
export function getTopPairs(
  matrix: CoOccurrenceMatrix,
  n: number = 50
): CoOccurrencePair[] {
  const allPairs: CoOccurrencePair[] = [];

  for (const innerMap of matrix.matrix.values()) {
    allPairs.push(...Array.from(innerMap.values()));
  }

  return allPairs.sort((a, b) => b.count - a.count).slice(0, n);
}

/**
 * Export matrix to CSV format
 */
export function exportMatrixToCSV(matrix: CoOccurrenceMatrix): string {
  const chars = matrix.characters;
  const rows: string[] = [];

  // Header row
  rows.push(['', ...chars].join(','));

  // Data rows
  for (const char1 of chars) {
    const row: (string | number)[] = [char1];

    for (const char2 of chars) {
      if (char1 === char2) {
        row.push('');
      } else {
        const pair = getCoOccurrencePair(matrix, char1, char2);
        row.push(pair ? pair.count : 0);
      }
    }

    rows.push(row.join(','));
  }

  return rows.join('\n');
}
