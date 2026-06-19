---
description: Clean Architecture layer boundaries and dependency rule
applyTo: "template/backend/src/**/*.py, scripts/**/*.py"
---

# Architecture Instructions

## Dependency Rule

- Dependencies must point inward toward domain policy layers.
- Inner layers never import outer layers.
- Keep presentation and infrastructure decoupled; orchestrate via application/core protocols.

## Layer Intent

- `core/`: domain entities, value objects, domain services, protocols
- `application/`: use-cases, orchestration, DTOs
- `infrastructure/`: protocol implementations, external systems
- `presentation/`: transport adapters (HTTP/CLI/GraphQL)
- `composition/`: dependency wiring only

## Enforced Practice

- Add or update architecture checks when introducing new directories/layers.
- Prefer protocol-first contracts in `core/` and adapter implementations in `infrastructure/`.
