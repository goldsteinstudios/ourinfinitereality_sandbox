import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { 
  insertChapterSchema, 
  insertCharacterSchema, 
  insertMappingSchema,
  updateMappingSchema,
  insertChapterProgressSchema 
} from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Chapters
  app.get("/api/chapters", async (req, res) => {
    try {
      const chapters = await storage.getAllChapters();
      res.json(chapters);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch chapters" });
    }
  });

  app.get("/api/chapters/:number", async (req, res) => {
    try {
      const number = parseInt(req.params.number);
      const chapter = await storage.getChapter(number);
      if (!chapter) {
        return res.status(404).json({ message: "Chapter not found" });
      }
      res.json(chapter);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch chapter" });
    }
  });

  app.post("/api/chapters", async (req, res) => {
    try {
      const chapterData = insertChapterSchema.parse(req.body);
      const chapter = await storage.createChapter(chapterData);
      res.status(201).json(chapter);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid chapter data", errors: error.errors });
      }
      res.status(500).json({ message: "Failed to create chapter" });
    }
  });

  // Characters
  app.get("/api/characters", async (req, res) => {
    try {
      const { search } = req.query;
      let characters;
      
      if (search && typeof search === 'string') {
        characters = await storage.searchCharacters(search);
      } else {
        characters = await storage.getAllCharacters();
      }
      
      res.json(characters);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch characters" });
    }
  });

  app.get("/api/characters/:char", async (req, res) => {
    try {
      const char = decodeURIComponent(req.params.char);
      const character = await storage.getCharacter(char);
      if (!character) {
        return res.status(404).json({ message: "Character not found" });
      }
      res.json(character);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch character" });
    }
  });

  app.post("/api/characters", async (req, res) => {
    try {
      const characterData = insertCharacterSchema.parse(req.body);
      const character = await storage.createCharacter(characterData);
      res.status(201).json(character);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid character data", errors: error.errors });
      }
      res.status(500).json({ message: "Failed to create character" });
    }
  });

  // Mappings
  app.post("/api/mappings", async (req, res) => {
    try {
      const mappingData = insertMappingSchema.parse({
        ...req.body,
        createdAt: new Date().toISOString()
      });
      const mapping = await storage.createMapping(mappingData);
      res.status(201).json(mapping);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid mapping data", errors: error.errors });
      }
      res.status(500).json({ message: "Failed to create mapping" });
    }
  });

  app.put("/api/mappings/:characterId", async (req, res) => {
    try {
      const characterId = parseInt(req.params.characterId);
      const updates = updateMappingSchema.parse(req.body);
      
      let mapping = await storage.getMapping(characterId);
      if (mapping) {
        mapping = await storage.updateMapping(characterId, updates);
      } else {
        mapping = await storage.createMapping({
          characterId,
          ...updates,
          createdAt: new Date().toISOString()
        });
      }
      
      res.json(mapping);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid mapping data", errors: error.errors });
      }
      res.status(500).json({ message: "Failed to update mapping" });
    }
  });

  app.delete("/api/mappings/:characterId", async (req, res) => {
    try {
      const characterId = parseInt(req.params.characterId);
      await storage.deleteMapping(characterId);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Failed to delete mapping" });
    }
  });

  // Chapter Progress
  app.put("/api/chapters/:number/progress", async (req, res) => {
    try {
      const chapterNumber = parseInt(req.params.number);
      const progressData = insertChapterProgressSchema.parse({
        ...req.body,
        chapterNumber
      });
      const progress = await storage.updateChapterProgress(progressData);
      res.json(progress);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid progress data", errors: error.errors });
      }
      res.status(500).json({ message: "Failed to update chapter progress" });
    }
  });

  // Lexicon stats
  app.get("/api/lexicon/stats", async (req, res) => {
    try {
      const stats = await storage.getLexiconStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch lexicon stats" });
    }
  });

  // Recent mappings
  app.get("/api/mappings/recent", async (req, res) => {
    try {
      const limit = req.query.limit ? parseInt(req.query.limit as string) : 10;
      const recent = await storage.getRecentMappings(limit);
      res.json(recent);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch recent mappings" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
