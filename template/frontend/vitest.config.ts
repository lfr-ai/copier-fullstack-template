/** Vitest test-runner configuration. */
import path from 'node:path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, 'src'),
    },
  },
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/unit/**/*.test.{ts,tsx}', 'tests/unit/**/*.spec.{ts,tsx}'],
    exclude: ['tests/e2e/**', 'node_modules/**'],
    typecheck: {
      enabled: true,
    },
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.d.ts', 'src/env.d.ts'],
      thresholds: {
        statements: 80,
        lines: 80,
        branches: 75,
        functions: 80,
      },
    },
  },
});
