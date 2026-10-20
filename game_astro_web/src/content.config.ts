import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';
import Papa from "papaparse";

// Define a `loader` and `schema` for each collection
const games = defineCollection({
  loader: glob({ base: './src/content', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
    title: z.string(),
    description: z.string(),
    image: image(),
    video: z.string(),
    type: z.string(),
  }),
});

const credits = defineCollection({
  loader: file("src/content/credits.csv", {
    parser: (text) =>
      Papa.parse<Record<string, string>>(text, {
        header: true,
        skipEmptyLines: true,
      }).data.map((row, i) => ({ id: String(i), ...row })),
  }),
});

export const collections = { games, credits };