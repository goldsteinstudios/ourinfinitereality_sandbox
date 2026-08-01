import { 
  chapters, 
  characters, 
  mappings, 
  chapterProgress,
  type Chapter, 
  type Character, 
  type Mapping, 
  type ChapterProgress,
  type InsertChapter, 
  type InsertCharacter, 
  type InsertMapping, 
  type InsertChapterProgress,
  type UpdateMapping,
  type CharacterWithMapping,
  type ChapterWithProgress
} from "@shared/schema";

export interface IStorage {
  // Chapters
  getAllChapters(): Promise<ChapterWithProgress[]>;
  getChapter(number: number): Promise<Chapter | undefined>;
  createChapter(chapter: InsertChapter): Promise<Chapter>;
  
  // Characters
  getAllCharacters(): Promise<CharacterWithMapping[]>;
  getCharacter(char: string): Promise<CharacterWithMapping | undefined>;
  getCharacterById(id: number): Promise<Character | undefined>;
  createCharacter(character: InsertCharacter): Promise<Character>;
  updateCharacterFrequency(char: string, frequency: number): Promise<void>;
  
  // Mappings
  getMapping(characterId: number): Promise<Mapping | undefined>;
  createMapping(mapping: InsertMapping): Promise<Mapping>;
  updateMapping(characterId: number, updates: UpdateMapping): Promise<Mapping | undefined>;
  deleteMapping(characterId: number): Promise<void>;
  
  // Chapter Progress
  getChapterProgress(chapterNumber: number): Promise<ChapterProgress | undefined>;
  updateChapterProgress(progress: InsertChapterProgress): Promise<ChapterProgress>;
  
  // Search and Analytics
  searchCharacters(query: string): Promise<CharacterWithMapping[]>;
  getLexiconStats(): Promise<{
    totalChars: number;
    mappedChars: number;
    pendingChars: number;
    progressPercent: number;
  }>;
  getRecentMappings(limit?: number): Promise<(Mapping & Character)[]>;
}

export class MemStorage implements IStorage {
  private chapters: Map<number, Chapter>;
  private characters: Map<string, Character>;
  private charactersById: Map<number, Character>;
  private mappings: Map<number, Mapping>;
  private chapterProgressMap: Map<number, ChapterProgress>;
  private currentChapterId: number;
  private currentCharacterId: number;
  private currentMappingId: number;
  private currentProgressId: number;

  constructor() {
    this.chapters = new Map();
    this.characters = new Map();
    this.charactersById = new Map();
    this.mappings = new Map();
    this.chapterProgressMap = new Map();
    this.currentChapterId = 1;
    this.currentCharacterId = 1;
    this.currentMappingId = 1;
    this.currentProgressId = 1;
  }

  async getAllChapters(): Promise<ChapterWithProgress[]> {
    return Array.from(this.chapters.values()).map(chapter => ({
      ...chapter,
      progress: this.chapterProgressMap.get(chapter.number) || null
    }));
  }

  async getChapter(number: number): Promise<Chapter | undefined> {
    return Array.from(this.chapters.values()).find(c => c.number === number);
  }

  async createChapter(insertChapter: InsertChapter): Promise<Chapter> {
    const id = this.currentChapterId++;
    const chapter: Chapter = { 
      ...insertChapter, 
      id,
      title: insertChapter.title || null
    };
    this.chapters.set(id, chapter);
    return chapter;
  }

  async getAllCharacters(): Promise<CharacterWithMapping[]> {
    const chars = Array.from(this.characters.values());
    return chars.map(char => ({
      ...char,
      mapping: this.mappings.get(char.id) || null,
      contexts: this.calculateContexts(char.character)
    }));
  }

  async getCharacter(char: string): Promise<CharacterWithMapping | undefined> {
    const character = this.characters.get(char);
    if (!character) return undefined;
    
    return {
      ...character,
      mapping: this.mappings.get(character.id) || null,
      contexts: this.calculateContexts(char)
    };
  }

  async getCharacterById(id: number): Promise<Character | undefined> {
    return this.charactersById.get(id);
  }

  async createCharacter(insertCharacter: InsertCharacter): Promise<Character> {
    const id = this.currentCharacterId++;
    const character: Character = { 
      ...insertCharacter, 
      id,
      frequency: insertCharacter.frequency || 0,
      firstChapter: insertCharacter.firstChapter || null
    };
    this.characters.set(character.character, character);
    this.charactersById.set(id, character);
    return character;
  }

  async updateCharacterFrequency(char: string, frequency: number): Promise<void> {
    const character = this.characters.get(char);
    if (character) {
      character.frequency = frequency;
    }
  }

  async getMapping(characterId: number): Promise<Mapping | undefined> {
    return this.mappings.get(characterId);
  }

  async createMapping(insertMapping: InsertMapping): Promise<Mapping> {
    const id = this.currentMappingId++;
    const mapping: Mapping = { 
      ...insertMapping, 
      id,
      literal: insertMapping.literal || null,
      philosophical: insertMapping.philosophical || null,
      contextual: insertMapping.contextual || null,
      notes: insertMapping.notes || null
    };
    this.mappings.set(insertMapping.characterId, mapping);
    return mapping;
  }

  async updateMapping(characterId: number, updates: UpdateMapping): Promise<Mapping | undefined> {
    const existing = this.mappings.get(characterId);
    if (!existing) return undefined;
    
    const updated: Mapping = { ...existing, ...updates };
    this.mappings.set(characterId, updated);
    return updated;
  }

  async deleteMapping(characterId: number): Promise<void> {
    this.mappings.delete(characterId);
  }

  async getChapterProgress(chapterNumber: number): Promise<ChapterProgress | undefined> {
    return this.chapterProgressMap.get(chapterNumber);
  }

  async updateChapterProgress(progress: InsertChapterProgress): Promise<ChapterProgress> {
    const existing = this.chapterProgressMap.get(progress.chapterNumber);
    const id = existing?.id || this.currentProgressId++;
    
    const updated: ChapterProgress = {
      id,
      ...progress,
      mappedCharacters: progress.mappedCharacters || 0,
      totalCharacters: progress.totalCharacters || 0,
      completionPercentage: (progress.totalCharacters || 0) > 0 
        ? Math.round((progress.mappedCharacters || 0) / (progress.totalCharacters || 0) * 100)
        : 0
    };
    
    this.chapterProgressMap.set(progress.chapterNumber, updated);
    return updated;
  }

  async searchCharacters(query: string): Promise<CharacterWithMapping[]> {
    const lowerQuery = query.toLowerCase();
    const chars = await this.getAllCharacters();
    
    return chars.filter(char => 
      char.character.includes(query) ||
      char.pinyin.toLowerCase().includes(lowerQuery) ||
      (char.mapping?.literal && char.mapping.literal.toLowerCase().includes(lowerQuery)) ||
      (char.mapping?.contextual && char.mapping.contextual.toLowerCase().includes(lowerQuery))
    );
  }

  async getLexiconStats(): Promise<{
    totalChars: number;
    mappedChars: number;
    pendingChars: number;
    progressPercent: number;
  }> {
    const chars = await this.getAllCharacters();
    const totalChars = chars.length;
    const mappedChars = chars.filter(c => c.mapping).length;
    const pendingChars = totalChars - mappedChars;
    const progressPercent = totalChars > 0 ? Math.round((mappedChars / totalChars) * 100) : 0;

    return {
      totalChars,
      mappedChars,
      pendingChars,
      progressPercent
    };
  }

  async getRecentMappings(limit = 10): Promise<(Mapping & Character)[]> {
    const mappings = Array.from(this.mappings.values())
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
      .slice(0, limit);

    return mappings.map(mapping => {
      const character = this.charactersById.get(mapping.characterId);
      return { ...mapping, ...character! };
    });
  }

  private calculateContexts(char: string): number {
    // Simple implementation - in a real app, this would analyze chapter contexts
    return Math.floor(Math.random() * 15) + 1;
  }
}

export const storage = new MemStorage();
