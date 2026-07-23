import { defineConfig } from 'eslint/config';
import js from '@eslint/js';
import * as astro from 'eslint-plugin-astro';
import ts from 'typescript-eslint';

export default defineConfig([
  js.configs.recommended,
  {
    ignores: ['dist/', '.astro/', 'node_modules/', '**/*.config.{js,mjs,ts}'],
  },
  {
    files: ['**/*.{ts,tsx,mts,cts}'],
    extends: [...ts.configs.recommended],
  },
  {
    files: ['**/*.astro'],
    extends: [...astro.configs.recommended],
  },
]);