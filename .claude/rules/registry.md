---
paths:
  - "template/registry/**/*.json"
  - "template/**/*registry*.{py,ts,tsx}"
---

# Registry Rules

- Update source registry data before touching generated constants.
- Regenerate derived constants after any registry edits.
- Avoid introducing duplicated naming constants outside registry flow.