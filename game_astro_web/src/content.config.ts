import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

// Define a `loader` and `schema` for each collection
const games = defineCollection({
  loader: glob({ base: './src/content', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
    title: z.string(),
    description: z.string(),
    image: image(),
    type: z.string(),
  }),
});

// Export a single `collections` object to register your collection(s)
export const collections = { games };