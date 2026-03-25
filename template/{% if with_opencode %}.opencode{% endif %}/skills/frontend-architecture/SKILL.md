---
name: frontend-architecture
description:
  Enforces clean frontend architecture patterns for TypeScript applications using React
  or Lit with Tailwind CSS v4 — validates separation of concerns, type safety, component
  patterns, state management, and data flow
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: architecture
  layer: frontend
---

## What I do

- Enforce clean separation of concerns in the frontend
- Validate component patterns (React functional components / Lit web components)
- Ensure proper TypeScript strict-mode usage
- Guide Tailwind v4 CSS-first configuration patterns
- Validate data flow (API → Zod validation → typed models → components)
- Ensure accessibility best practices

## Frontend Architecture Layers

```
api/          → Backend communication. Typed fetch wrappers. ZERO UI logic.
models/       → Zod schemas + TypeScript types. Runtime validation contracts.
                schemas/ → Zod runtime schemas with inferred types
                types/   → Pure TypeScript interfaces (no runtime deps)
features/     → Feature modules. Each feature owns components, hooks, stores.
hooks/        → Shared React hooks / Lit reactive controllers.
stores/       → Global state management (signals / zustand / nanostores).
lib/          → Pure utility functions. ZERO side effects. ZERO imports from UI.
config/       → Runtime environment configuration. Build-time env vars.
components/   → Shared UI components (common/, layout/, ui/).
styles/       → Tailwind v4 CSS-first config, global styles.
router/       → Application routing configuration.
```

## Rules I Enforce

### React Patterns (when `frontend_framework == 'react'`)

- Functional components only — no class components
- All props typed with `interface` (not `type`)
- `React.StrictMode` wrapping the root
- `ErrorBoundary` wrapping route trees
- `Suspense` with fallback for lazy-loaded routes
- TanStack Query for server state (no manual `useEffect` for fetches)
- Zod schemas validate all API responses before use
- Custom hooks extract reusable logic from components
- `React.lazy()` for route-level code splitting

### Lit Patterns (when `frontend_framework == 'lit'`)

- `@customElement` decorator for all components
- `@property()` and `@state()` decorators for reactive properties
- Lit Router (`@lit-labs/router`) for SPA routing
- Lit Context (`@lit/context`) for dependency injection
- Lit Task (`@lit/task`) for async data loading
- Reactive controllers for reusable stateful logic
- CSS-in-JS via `static styles = css\`...\``
- Shadow DOM for encapsulation

### Tailwind CSS v4 Patterns

- CSS-first configuration via `@theme {}` block
- `@layer base`, `@layer components`, `@layer utilities` for custom styles
- CSS custom properties (design tokens) in `@theme`
- Dark mode via `@media (prefers-color-scheme: dark)` + `@theme` overrides
- No `tailwind.config.js` (v4 uses CSS-only config)
- Container queries via `@container`

### Data Flow

```
API response → Zod .parse() → Typed model → Component props → Render
                                    ↑
                              Store (global state)
```

### Strict Prohibitions

- NO `any` type — use `unknown` or proper generics
- NO inline styles — use Tailwind utility classes or `static styles`
- NO `document.querySelector` in React — use refs
- NO untrusted HTML injection — sanitize or use framework escaping
- NO API calls in components — use hooks/controllers/services
- NO business logic in components — extract to hooks/lib/services

## When to use me

Use this skill when:

- Creating new frontend components
- Setting up routing or data fetching
- Reviewing frontend architecture
- Adding state management
- Configuring Tailwind v4 themes
- Adding accessibility features
