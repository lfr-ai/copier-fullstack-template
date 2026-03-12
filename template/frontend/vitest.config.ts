/**
 * @module vitest.config
 *
 * Vitest test-runner configuration.
 *
 * - Uses **happy-dom** as the DOM environment.
 * - Runs all `tests/unit/**` files; excludes `tests/e2e`.
 * - V8 code-coverage provider scoped to source TypeScript files.
 * - Global setup file: `tests/setup.ts`.
 */
import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "src"),
    },
  },
  test: {
    globals: true,
    environment: "happy-dom",
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/unit/**/*.test.ts", "tests/unit/**/*.spec.ts"],
    exclude: ["tests/e2e/**", "node_modules/**"],
    coverage: {
      provider: "v8",
      include: ["src/**/*.ts"],
      exclude: ["src/**/*.d.ts", "src/vite-env.d.ts"],
      thresholds: {
        statements: 80,
        lines: 80,
      },
    },
  },
});
