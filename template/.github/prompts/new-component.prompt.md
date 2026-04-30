---
description: 'Create a new React component using shadcn/ui primitives and project patterns'
name: 'new-component'
argument-hint: 'Component name and purpose (e.g., UserCard displays user profile summary)'
agent: 'agent'
model: 'Claude Sonnet 4'
tools:
  [
    search/codebase,
    search/fileSearch,
    read/readFile,
    edit/editFiles,
    execute/runInTerminal,
    shadcn/*,
    context7/get-library-docs,
    context7/resolve-library-id,
  ]
---

# New React Component

Create a new React component following project frontend conventions.

## Steps

1. **Check shadcn/ui** — Determine if existing primitives can be composed
2. **Create component** — In the appropriate directory under `frontend/src/presentation/components/`
3. **Add types** — Define props interface with JSDoc
4. **Write tests** — Using Vitest + React Testing Library
5. **Export** — Add to barrel exports if applicable

## Conventions

- Use TypeScript strict mode
- Use `cn()` utility for conditional class merging
- Use Tailwind CSS v4 classes (oklch color tokens)
- Prefer composition of shadcn/ui primitives over custom HTML
- Use `cva` (class-variance-authority) for variant props
- Keep components under 150 lines — extract sub-components if larger
- Use `React.forwardRef` for components accepting refs

## File Structure

```text
frontend/src/presentation/components/
├── ui/           # shadcn/ui primitives (don't modify directly)
├── common/       # Shared domain components
├── layout/       # Layout components
└── features/     # Feature-specific components
```

## Verification

```bash
task frontend:lint && task frontend:typecheck && task frontend:test:unit
```
