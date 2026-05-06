---
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
  - "frontend/**/*.css"
---

# Frontend Conventions

- Use TypeScript strict mode — no `any`, no type assertions unless unavoidable
- Use shadcn/ui primitives as base components (don't re-implement from scratch)
- Use `cn()` utility from `lib/utils` for conditional class merging
- Use Tailwind CSS v4 with oklch color tokens
- Use Biome for linting and formatting (not ESLint/Prettier)
- Use React Hook Form + Zod for form validation
- Use TanStack Query for server state
- Use Zustand for client-only state
- Components go in `presentation/components/` (ui/, common/, layout/, features/)
- Keep components under 150 lines — extract sub-components when larger
- Use `React.forwardRef` for components accepting refs (or pass `ref` as a prop in React 19+)
- Name files in kebab-case: `user-profile-card.tsx`
