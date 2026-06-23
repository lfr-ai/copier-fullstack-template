---
name: ui-ux-frontend
description: Frontend UX, accessibility, responsive layout, and Storybook interaction quality standards.
applyTo: "frontend/**/*.{ts,tsx,css,mdx}"
---

# UI UX Frontend Skill

## Purpose

Use this skill when implementing or reviewing user-facing frontend behavior.

## Standards

- Prioritize clear information architecture and interaction predictability.
- Validate keyboard flow and visible focus states on interactive controls.
- Ensure accessible names for icon-only controls.
- Keep spacing and typography consistent with design tokens.
- Verify loading, empty, success, and error states.
- Keep interactions observable and testable in Storybook and unit tests.

## Storybook Alignment

- Add focused stories for each significant UX state.
- Add `play` functions for critical interactions.
- Keep stories and docs useful for agentic manifests (clear names and summaries).

## Quick Checklist

- [ ] Responsive at mobile/tablet/desktop breakpoints
- [ ] Contrast and focus visibility acceptable
- [ ] Error messaging actionable and specific
- [ ] Keyboard and screen-reader paths tested
- [ ] Storybook story coverage added for changed UI# UI/UX Frontend Skill

Use this skill when implementing or reviewing frontend UX flows, visual
hierarchy, interaction behavior, and accessibility details in generated projects.

## Scope

- Form usability (labels, hints, validation feedback, focus management)
- Information hierarchy and progressive disclosure
- Responsive behavior across common breakpoints
- Keyboard navigation and screen reader compatibility
- Empty/loading/error/success state clarity

## Working Rules

1. Keep components thin: presentation only, delegate side effects to
   application hooks.
2. Favor existing shadcn/ui primitives before introducing custom components.
3. Prefer `getByRole` and semantic HTML patterns for testability and
   accessibility.
4. Keep cognitive load low: short components, named conditionals, early returns.
5. Preserve clean architecture import boundaries.

## Validation Checklist

- Visual and interaction behavior matches expected user journey.
- WCAG 2.1 AA critical checks pass (focus order, labels,
  contrast-sensitive states).
- Unit/integration tests cover important interaction states.
- Project quality gates pass.
