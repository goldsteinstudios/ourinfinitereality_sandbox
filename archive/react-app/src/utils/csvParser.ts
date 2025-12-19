import Papa from 'papaparse';
import type { Character, CharacterData, CharacterOccurrence } from '../types';

export interface ParsedCSVData {
  characters: Character[];
  characterMap: Map<string, CharacterData>;
  grid: (Character | null)[][]; // grid[chapter][position]
}

export async function parseCSV(file: string): Promise<ParsedCSVData> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      download: true,
      header: false,
      skipEmptyLines: false,
      complete: (results) => {
        try {
          const parsed = processCSVData(results.data as string[][]);
          resolve(parsed);
        } catch (error) {
          reject(error);
        }
      },
      error: (error: Error) => {
        reject(error);
      }
    });
  });
}

function processCSVData(data: string[][]): ParsedCSVData {
  const characters: Character[] = [];
  const characterMap = new Map<string, CharacterData>();

  // CSV structure: 163 columns
  // Column 0: "Loc" (position/row number)
  // Columns 1, 3, 5, ..., 161 (odd indices): Chinese characters for chapters 1-81
  // Columns 2, 4, 6, ..., 162 (even indices): Pinyin for chapters 1-81

  const header = data[0];
  const rows = data.slice(1); // Skip header row

  // Initialize grid: 81 chapters × max positions
  const grid: (Character | null)[][] = Array(81).fill(null).map(() => []);

  rows.forEach((row, rowIndex) => {
    const position = rowIndex + 1; // Position is 1-indexed
    const locationValue = row[0];

    // Process each chapter (81 chapters)
    for (let chapterNum = 1; chapterNum <= 81; chapterNum++) {
      // Calculate column indices
      // Chapter 1: columns 1 (char) and 2 (pinyin)
      // Chapter 2: columns 3 (char) and 4 (pinyin)
      // Chapter N: columns (2*N-1) and (2*N)
      const charColIndex = 2 * chapterNum - 1;
      const pinyinColIndex = 2 * chapterNum;

      const char = row[charColIndex]?.trim();
      const pinyin = row[pinyinColIndex]?.trim() || '';

      if (char && char !== '') {
        const character: Character = {
          char,
          pinyin,
          chapter: chapterNum,
          position,
        };

        characters.push(character);
        grid[chapterNum - 1][position - 1] = character;

        // Update character map for occurrence tracking
        const key = char;
        if (!characterMap.has(key)) {
          characterMap.set(key, {
            character: char,
            pinyin,
            occurrences: []
          });
        }

        characterMap.get(key)!.occurrences.push({
          chapter: chapterNum,
          position
        });
      } else {
        // Empty cell
        grid[chapterNum - 1][position - 1] = null;
      }
    }
  });

  return {
    characters,
    characterMap,
    grid
  };
}

export function getCharacterOccurrences(
  characterMap: Map<string, CharacterData>,
  char: string
): CharacterOccurrence[] {
  return characterMap.get(char)?.occurrences || [];
}
