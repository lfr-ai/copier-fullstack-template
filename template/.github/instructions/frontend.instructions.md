---
description: Frontend TypeScript, component patterns, and Vite build conventions
applyTo: "frontend/**/*.ts, frontend/**/*.tsx, frontend/**/*.css"
---

- Strict TypeScript (`strict: true`) — no `any`, use `unknown` or proper generics
- Functional components with typed props interfaces
- Tailwind CSS v4 for styling (`@theme {}`, `@layer components`)
- Vite for build tooling with `manualChunks` vendor splitting
- `lightningcss` for CSS processing
- Bun for package management and JavaScript runtime
- Biome for linting and formatting (replaces ESLint + Prettier)
- Vitest for unit tests (happy-dom environment)

- React: TanStack Query for server state, React Router for navigation,
  ErrorBoundary + Suspense for loading/error states, React Aria for accessibility,
  React Hook Form + Zod for form validation

- Mirror source structure in `frontend/tests/unit/`
- Component tests verify render output and user interactions
- Use `vi.mock()` for module-level mocks
- Use `vi.fn()` for function mocks
- Setup file at `frontend/tests/setup.ts` handles DOM cleanup and browser API stubs

- Use named exports, avoid default exports
- Colocate types with their modules
- Use `const` assertions for literal objects
- Destructure props in function signatures
- Template literals over string concatenation
