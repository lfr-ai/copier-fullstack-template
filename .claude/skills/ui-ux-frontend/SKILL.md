# UI/UX Frontend Skill

Use this skill when implementing or reviewing frontend UX flows, visual hierarchy,
interaction behavior, and accessibility details.

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
