---
description: Frontend TypeScript, shadcn/ui, Storybook, and Playwright conventions for template frontend work
applyTo: "template/frontend/**/*.{ts,tsx,css,json}"
---

- Prefer shadcn/ui primitives first; avoid custom styled markup when equivalent
  primitives exist.
- Keep TypeScript strict and avoid `any`; use explicit interfaces and generics.
- Keep semantic design tokens; avoid hardcoded visual colors when token classes
  exist.
- Keep Storybook configured for React + Vite and maintain useful manifests for
  agent workflows.
- Add Storybook stories for reusable UI primitives and complex domain components.
- Add `play` interaction tests for critical UX flows in stories where relevant.
- Keep stories focused (one concept per story) and include JSDoc summaries for
  components and stories so manifests remain useful for agent workflows.
- Use `!manifest` tags to exclude instructional-only stories/docs from AI
  manifests.
- Use Playwright for end-to-end user journeys and accessibility-focused checks.
- Prefer Playwright selectors in this order: `getByRole`, `getByLabel`,
  `getByText`, then `getByTestId`.
- Keep frontend architecture layered (`application`, `domain`, `infrastructure`,
  `presentation`) with clear boundaries.
