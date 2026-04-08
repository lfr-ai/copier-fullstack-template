---
description: Frontend TypeScript, component patterns, and Vite build conventions
applyTo: "frontend/**/*.ts, frontend/**/*.tsx, frontend/**/*.css"
---

- Prefer shadcn/ui components first; avoid custom styled markup when an equivalent
    primitive exists (Button, Card, Dialog, DropdownMenu, Input, Badge, Separator,
    Skeleton, etc.)
- Before creating/editing UI patterns, consult shadcn docs via Context7 or
    shadcn MCP context for current component API and composition rules
- Use strict TypeScript ('strict: true') — no 'any', use 'unknown' or proper
    generics
- Use functional components with typed props interfaces
- Use named exports; avoid default exports in application code

- Use Tailwind CSS v4 in CSS-first mode (`@import "tailwindcss"`, `@theme inline`)
- Keep all theme tokens in one global stylesheet and use semantic classes
    ('bg-background', 'text-foreground', 'border-border', 'ring-ring')
- Never hardcode visual colors in component classes when semantic tokens exist
- Keep dark mode class-based (`.dark`) and controlled through `ThemeProvider`

- Use Vite for build tooling with explicit aliases and predictable chunking
- Keep `moduleResolution: bundler` and strict TS compiler options enabled
- Use `lightningcss` and keep plugin list minimal for fast startup
- Avoid unnecessary barrel files in hot paths to improve Vite performance

- Use Bun for package management/runtime
- Use Biome for linting + formatting
- Use Vitest (happy-dom) for unit tests

- React Hook Form + Zod for form validation and schemas
- TanStack Query for server state fetching and caching
- React Router for navigation (prefer NavLink for primary nav)
- ErrorBoundary + Suspense for loading/error states
- React Router mode guidance: keep declarative routing as template default
    (`BrowserRouter` + `Routes`) and adopt data routers only when loaders/actions
    or pending UI semantics are required
- React Router: prefer `NavLink` for primary navigation (active state +
    `aria-current`); use `Link` for neutral links; reserve `useNavigate` for
    programmatic transitions only (post-submit, timeout, auth redirect)
- React Hook Form: prefer `Controller` for controlled shadcn/radix components,
    stable `defaultValues`, and explicit `aria-invalid` + field-level error text
- React Hook Form: keep schema and form value types colocated and derived from Zod
    (`z.infer<typeof schema>`) for single-source typing
- shadcn forms: prefer scaffolded field primitives (Input/Label/Textarea/Select,
    etc.) and semantic invalid states (`data-invalid`, `text-destructive`)
- Declare `lazy()` imports at module scope only and wrap with meaningful Suspense
    boundaries

- Mirror source structure in `frontend/tests/unit/`
- Component tests verify render output and user interactions
- Use `vi.mock()` for module-level mocks
- Use `vi.fn()` for function mocks
- Keep setup behavior in `frontend/tests/setup.ts`

- Keep imports extension-consistent and alias-driven (`@/...`)
- Colocate types with their modules
- Use `const` assertions for literal objects
- Destructure props in function signatures
- Prefer template literals over string concatenation
