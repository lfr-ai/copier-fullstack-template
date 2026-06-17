---
description: Test strategy and quality standards
applyTo: "**/tests/**/*.py, **/*test*.ts, **/*test*.tsx"
---

# Testing Instructions

- Use the appropriate test level: unit, integration, property, or e2e.
- Keep tests isolated and avoid hidden global state.
- Validate edge cases and failure paths, not just happy paths.
- Prefer fixtures/factories over repetitive inline setup.
- Keep tests readable: arrange, act, assert.