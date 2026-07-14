import { defineCollection, z } from 'astro:content';

const translations = defineCollection({
  type: 'content',
  schema: z.object({
    chapter: z.number(),
    chineseTitle: z.string(),
    englishTitle: z.string(),
    version: z.string(),
    lastUpdated: z.string(),
    rsmVersion: z.string().optional(),
    confidence: z.enum(['strong', 'plausible', 'speculative']).optional(),
    confidenceNotes: z.array(z.object({
      element: z.string(),
      level: z.enum(['strong', 'plausible', 'speculative']),
      note: z.string(),
    })).default([]),
    changes: z.array(z.object({
      version: z.string(),
      date: z.string(),
      notes: z.string(),
    })).default([]),
    tags: z.array(z.string()).default([]),
  }),
});

const objects = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    title: z.string(),
    subtitle: z.string().optional(),
    depth: z.number(),
    domain: z.enum(['ddj', 'biology', 'physics', 'pattern']),
    deeper: z.array(z.string()).default([]),
    lateral: z.array(z.string()).default([]),
    surface: z.array(z.string()).default([]),
    icon: z.string().optional(),
    source: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});

const essays = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    description: z.string(),
    readTime: z.string(),
    date: z.string().optional(),
    order: z.number().default(99),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { objects, essays, translations };
