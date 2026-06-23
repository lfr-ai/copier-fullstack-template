# UI UX Frontend Skill

## Scope

Apply this skill when improving or reviewing frontend user experience quality.

## Goals

- Improve accessibility and interaction clarity.
- Keep responsive behavior consistent.
- Ensure Storybook states represent real user flows.

## Checklist

- [ ] Keyboard navigation works end-to-end
- [ ] Focus indicators are visible and consistent
- [ ] Empty/loading/error/success states are explicit
- [ ] Stories cover critical interaction paths
- [ ] UI copy and labels are specific and concise# UI/UX Frontend Skill

Use this skill when implementing or reviewing frontend UX flows, visual hierarchy,
interaction behavior, and accessibility details in generated projects.

## Scope

- Form usability (labels, hints, validation, focus management)
- Information hierarchy and progressive disclosure
- Responsive behavior across breakpoints
- Keyboard navigation and screen reader compatibility
- Empty/loading/error/success state clarity
- Storybook play-function interaction quality and manifest usefulness

## Working Rules

1. Keep components thin; delegate side effects to application hooks.
2. Prefer existing shadcn/ui primitives before custom components.
3. Prefer semantic HTML and role/label-based queries for accessibility and tests.
4. Keep cognitive load low with short components, named conditionals, and early returns.
5. Preserve clean-architecture import boundaries.

## Validation Checklist

- UX flow supports success and failure paths
- WCAG 2.1 AA essentials pass (focus, labels, contrast-sensitive states)
- Storybook stories include representative states and interaction tests where useful
- Project quality gates pass
