---
description: UI/UX quality, accessibility, and story-driven interaction conventions
applyTo: "frontend/**/*.{ts,tsx,css,mdx}"
---

- Design for clarity first: meaningful visual hierarchy, concise copy, and predictable actions.
- Keep components keyboard-accessible and screen-reader-friendly by default.
- Prefer semantic HTML and ARIA only where semantics are insufficient.
- Use Storybook stories for reusable components and include interaction coverage for critical flows.
- Keep one story = one intent; avoid overloaded showcase stories.
- Add concise story and component descriptions that explain why a pattern should be used.
- Use `play` interaction tests for high-impact UX behavior.
- For responsive behavior, verify mobile, tablet, and desktop breakpoints in stories or tests.
- Avoid color-only affordances; ensure contrast and state cues are perceivable.
- Keep empty/error/loading states explicit and humane.