import { defineCollection, z } from 'astro:content';

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

export const collections = { objects, essays };
