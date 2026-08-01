import { pgTable, text, serial, integer, boolean, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const chapters = pgTable("chapters", {
  id: serial("id").primaryKey(),
  number: integer("number").notNull().unique(),
  chineseText: text("chinese_text").notNull(),
  pinyin: text("pinyin").notNull(),
  title: text("title"),
});

export const characters = pgTable("characters", {
  id: serial("id").primaryKey(),
  character: text("character").notNull().unique(),
  pinyin: text("pinyin").notNull(),
  frequency: integer("frequency").default(0),
  firstChapter: integer("first_chapter"),
});

export const mappings = pgTable("mappings", {
  id: serial("id").primaryKey(),
  characterId: integer("character_id").notNull(),
  literal: text("literal"),
  philosophical: text("philosophical"),
  contextual: text("contextual"),
  notes: text("notes"),
  createdAt: text("created_at").notNull(),
});

export const chapterProgress = pgTable("chapter_progress", {
  id: serial("id").primaryKey(),
  chapterNumber: integer("chapter_number").notNull().unique(),
  mappedCharacters: integer("mapped_characters").default(0),
  totalCharacters: integer("total_characters").default(0),
  completionPercentage: integer("completion_percentage").default(0),
});

// Insert schemas
export const insertChapterSchema = createInsertSchema(chapters).omit({ id: true });
export const insertCharacterSchema = createInsertSchema(characters).omit({ id: true });
export const insertMappingSchema = createInsertSchema(mappings).omit({ id: true });
export const insertChapterProgressSchema = createInsertSchema(chapterProgress).omit({ id: true });

// Update schemas
export const updateMappingSchema = createInsertSchema(mappings).omit({ id: true, characterId: true, createdAt: true });

// Types
export type Chapter = typeof chapters.$inferSelect;
export type Character = typeof characters.$inferSelect;
export type Mapping = typeof mappings.$inferSelect;
export type ChapterProgress = typeof chapterProgress.$inferSelect;

export type InsertChapter = z.infer<typeof insertChapterSchema>;
export type InsertCharacter = z.infer<typeof insertCharacterSchema>;
export type InsertMapping = z.infer<typeof insertMappingSchema>;
export type InsertChapterProgress = z.infer<typeof insertChapterProgressSchema>;
export type UpdateMapping = z.infer<typeof updateMappingSchema>;

// Extended types for API responses
export type CharacterWithMapping = Character & {
  mapping?: Mapping | null;
  contexts: number;
};

export type ChapterWithProgress = Chapter & {
  progress: ChapterProgress | null;
};
