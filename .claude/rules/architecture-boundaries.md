---
paths:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.tsx"
---

# Architecture Boundaries

Enforce strict inward dependency flow:

```text
Presentation → Application → Domain ← Infrastructure
```

## Layer boundaries

- Domain: pure types and business rules only.
- Application: use-case orchestration and state transitions.
- Infrastructure: external systems and adapters.
- Presentation: rendering and user interactions.
- Shared/Lib: cross-cutting utilities without business coupling.

## Import direction

- Domain imports nothing from other layers.
- Application imports Domain only.
- Infrastructure imports Domain only.
- Presentation imports Application and Domain.
- Lib imports no application-specific modules.

## Operational rules

- Keep side effects outside domain and presentation rendering logic.
- Reject circular dependencies.
- Favor explicit contracts between layers.
