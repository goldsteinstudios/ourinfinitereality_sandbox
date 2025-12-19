import type { Character, CharacterOccurrence } from '../types';
import type { ContextWindow } from '../types/analysis';
import type { ParsedCSVData } from './csvParser';

/**
 * Extract context window around a specific character occurrence
 */
export function extractContextWindow(
  data: ParsedCSVData,
  occurrence: CharacterOccurrence,
  windowSize: number = 5
): ContextWindow | null {
  const { grid } = data;
  const { chapter, position } = occurrence;

  // Get the chapter data (0-indexed)
  const chapterData = grid[chapter - 1];
  if (!chapterData) return null;

  // Get the character at this position (0-indexed)
  const character = chapterData[position - 1];
  if (!character) return null;

  // Extract characters before
  const before: Character[] = [];
  for (let i = position - windowSize; i < position; i++) {
    if (i >= 1) {
      const char = chapterData[i - 1];
      if (char) before.push(char);
    }
  }

  // Extract characters after
  const after: Character[] = [];
  for (let i = position + 1; i <= position + windowSize; i++) {
    if (i <= chapterData.length) {
      const char = chapterData[i - 1];
      if (char) after.push(char);
    }
  }

  return {
    character,
    before,
    after,
    windowSize,
    chapter,
    position,
  };
}

/**
 * Extract all context windows for a given character
 */
export function extractAllContexts(
  data: ParsedCSVData,
  char: string,
  windowSize: number = 5
): ContextWindow[] {
  const characterData = data.characterMap.get(char);
  if (!characterData) return [];

  const contexts: ContextWindow[] = [];
  for (const occurrence of characterData.occurrences) {
    const context = extractContextWindow(data, occurrence, windowSize);
    if (context) {
      contexts.push(context);
    }
  }

  return contexts;
}

/**
 * Format context window as text string
 */
export function formatContextWindow(
  context: ContextWindow,
  options: {
    showChapter?: boolean;
    showPosition?: boolean;
    highlightCenter?: boolean;
    separator?: string;
  } = {}
): string {
  const {
    showChapter = false,
    showPosition = false,
    highlightCenter = false,
    separator = ' ',
  } = options;

  const beforeText = context.before.map(c => c.char).join('');
  const centerText = context.character.char;
  const afterText = context.after.map(c => c.char).join('');

  let result = '';

  if (showChapter || showPosition) {
    const location = [];
    if (showChapter) location.push(`Ch ${context.chapter}`);
    if (showPosition) location.push(`Pos ${context.position}`);
    result += `[${location.join(', ')}]${separator}`;
  }

  if (highlightCenter) {
    result += `${beforeText}${separator}[${centerText}]${separator}${afterText}`;
  } else {
    result += `${beforeText}${centerText}${afterText}`;
  }

  return result;
}

/**
 * Find characters in context that match a specific character
 */
export function findInContext(
  context: ContextWindow,
  searchChar: string
): { before: number[]; after: number[] } {
  const beforeIndices: number[] = [];
  const afterIndices: number[] = [];

  context.before.forEach((char, index) => {
    if (char.char === searchChar) {
      beforeIndices.push(index);
    }
  });

  context.after.forEach((char, index) => {
    if (char.char === searchChar) {
      afterIndices.push(index);
    }
  });

  return { before: beforeIndices, after: afterIndices };
}

/**
 * Check if two characters co-occur within a context window
 */
export function checkCoOccurrenceInContext(
  context: ContextWindow,
  char1: string,
  char2: string
): boolean {
  const allChars = [
    ...context.before,
    context.character,
    ...context.after,
  ];

  const hasChar1 = allChars.some(c => c.char === char1);
  const hasChar2 = allChars.some(c => c.char === char2);

  return hasChar1 && hasChar2;
}

/**
 * Get distance between two characters in context
 * Returns null if either character is not in the context
 */
export function getDistanceInContext(
  context: ContextWindow,
  char1: string,
  char2: string
): number | null {
  const allChars = [
    ...context.before,
    context.character,
    ...context.after,
  ];

  const index1 = allChars.findIndex(c => c.char === char1);
  const index2 = allChars.findIndex(c => c.char === char2);

  if (index1 === -1 || index2 === -1) return null;

  return Math.abs(index2 - index1);
}

/**
 * Extract a larger context (cross-chapter if needed)
 */
export function extractExtendedContext(
  data: ParsedCSVData,
  occurrence: CharacterOccurrence,
  windowSize: number = 10
): Character[] {
  const { grid, characters } = data;
  const { chapter, position } = occurrence;

  // Find the character in the flat array
  const targetIndex = characters.findIndex(
    c => c.chapter === chapter && c.position === position
  );

  if (targetIndex === -1) return [];

  const startIndex = Math.max(0, targetIndex - windowSize);
  const endIndex = Math.min(characters.length - 1, targetIndex + windowSize);

  return characters.slice(startIndex, endIndex + 1);
}

/**
 * Compare two contexts to find patterns
 */
export function compareContexts(
  context1: ContextWindow,
  context2: ContextWindow
): {
  similarity: number;
  commonBefore: string[];
  commonAfter: string[];
} {
  const before1 = new Set(context1.before.map(c => c.char));
  const before2 = new Set(context2.before.map(c => c.char));
  const after1 = new Set(context1.after.map(c => c.char));
  const after2 = new Set(context2.after.map(c => c.char));

  const commonBefore = Array.from(before1).filter(c => before2.has(c));
  const commonAfter = Array.from(after1).filter(c => after2.has(c));

  const totalBefore = before1.size + before2.size;
  const totalAfter = after1.size + after2.size;
  const totalCommon = commonBefore.length + commonAfter.length;
  const total = totalBefore + totalAfter;

  const similarity = total > 0 ? (totalCommon * 2) / total : 0;

  return {
    similarity,
    commonBefore,
    commonAfter,
  };
}
