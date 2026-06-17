---
paths:
  - "template/backend/src/**/core/**/*.py"
  - "template/backend/src/**/application/**/*.py"
---

# DDD Rules

- Keep ubiquitous language stable across entities/services/use-cases.
- Place invariants in domain entities/value objects where possible.
- Keep orchestration logic in application layer, not in presentation adapters.