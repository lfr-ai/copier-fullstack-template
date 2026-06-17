---
description: Reduce cognitive load via clarity-first code structure
applyTo: "**/*.{py,ts,tsx,js,jsx}"
---

# Cognitive Load Instructions

- Prefer early returns over deep nesting.
- Name intermediate boolean conditions.
- Keep related logic co-located; avoid context hopping.
- Avoid abstraction for single-use logic unless it improves readability.
- Favor small, deep modules over large, shallow wrappers.
- Comments should explain _why_, not restate _what_.