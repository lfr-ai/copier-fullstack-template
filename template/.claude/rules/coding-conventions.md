---
paths:
  - "**/*.{py,ts,tsx,js,jsx,md,yml,yaml,toml,json}"
---

# Coding Conventions

- Keep changes minimal, explicit, and type-safe.
- Prefer clear names over abbreviations.
- Remove dead code in the same change set.
- Use structured logging; avoid ad-hoc prints in production paths.
- Keep functions cohesive and short; extract intent-revealing helpers.
- Include tests for behavior changes and update docs for contract/config changes.
