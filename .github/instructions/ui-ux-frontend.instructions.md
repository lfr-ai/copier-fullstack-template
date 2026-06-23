---
description: UI/UX interaction, accessibility, and responsive conventions for frontend work
applyTo: "**/*.{ts,tsx,css,md}"
---

- Prioritize semantic HTML and accessible roles before custom ARIA.
- Keep focus order logical and preserve visible focus indicators.
- Ensure forms expose labels, hints, and actionable error messages.
- Design for loading/empty/error/success states explicitly.
- Keep interactions keyboard-friendly (Tab, Enter, Escape, arrow keys where relevant).
- Prefer Storybook stories with representative UX states and meaningful `play` interactions.
- Prefer Testing Library queries by role/label/text; use test ids as last resort.
- Preserve low cognitive load: concise components, named booleans, early returns.
- Keep responsive behavior explicit across small/medium/large breakpoints.
