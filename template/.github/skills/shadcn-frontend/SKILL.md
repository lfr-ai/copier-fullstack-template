---
name: shadcn-frontend
description: >
  Enforces shadcn/ui-first frontend implementation with React + Vite + TypeScript.
  Use when creating or refactoring UI components, forms, layouts, or theming.
---

# Skill: shadcn Frontend

## Purpose

Standardize frontend work around shadcn/ui, semantic design tokens, and
production-grade React + Vite + TypeScript patterns.

## Use This Skill When

- Building or refactoring React UI
- Adding pages, layouts, forms, or dialogs
- Extending design system tokens and component primitives
- Reviewing accessibility and composition quality

## Rules

- Prefer shadcn/ui components over bespoke styled markup
- Use Context7, shadcn MCP, or official upstream docs before composing new
  UI patterns or router/form architecture changes
- Use shadcn documentation/MCP context before implementing new component patterns
  or form compositions
- Keep components in `src/presentation/components/ui/` aligned with shadcn patterns
- Use semantic Tailwind tokens (`bg-background`, `text-foreground`, etc.)
- Use `asChild` for composable triggers and link-like buttons
- Prefer React Router `NavLink` for primary nav and active states;
  use `useNavigate` only for non-click programmatic transitions
- Keep declarative React Router as default scaffold and use data routers only when
  loaders/actions or revalidation features are required
- Keep theme tokens in `src/presentation/styles/tailwind.css`
- Keep dark mode class-based and controlled by `ThemeProvider`
- Prefer named exports for pages/components
- Keep strict TypeScript; do not use `any`
- Build forms with React Hook Form + Zod; use `Controller` for controlled
  shadcn/radix inputs and expose field errors accessibly (`aria-invalid`, alerts)
- **Never use TanStack Form** — Use React Hook Form + Zod for all form validation.
  TanStack Query is for server state (fetching, caching), not forms.
- Derive form value types directly from schemas (`z.infer<typeof schema>`) and keep
  schema + defaults colocated
- Add/modify components via shadcn CLI scripts before hand-editing from scratch
- Preserve accessibility structure (`DialogTitle`, labels, keyboard navigation)

## Verification Commands

- `bun run lint`
- `bun run typecheck`
- `bun run test`
- `bun run ui:info`
