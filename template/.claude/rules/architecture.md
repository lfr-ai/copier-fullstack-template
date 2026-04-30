---
paths:
  - "**"
---

# Architecture Rules

## Dependency Rule (NEVER violate)

Inner layers must never import from outer layers:

```
core/ <- application/ <- infrastructure/
                      <- presentation/
                      <- composition/
```

## Layer Responsibilities

- **core/** — Domain entities, value objects, interfaces, domain services, domain events
- **application/** — Use case orchestration, CQRS commands/queries, DTOs, mappers
- **infrastructure/** — Database (SQLAlchemy), cache (Redis), external APIs, file storage
- **presentation/** — FastAPI routes, Pydantic schemas, middleware, CLI commands
- **composition/** — Dependency injection container, app factory wiring

## Import Rules

- `core/` imports: stdlib only + domain libraries (no framework imports)
- `application/` imports: `core/` only
- `infrastructure/` imports: `core/` + external libraries (SQLAlchemy, Redis, httpx)
- `presentation/` imports: `application/` + `core/` + framework (FastAPI, Pydantic)
- `composition/` imports: everything (it's the wiring layer)

## Patterns

- Repository Pattern for data access (interface in core, implementation in infrastructure)
- Unit of Work for transaction management
- CQRS for separating read/write operations
- Domain Events for cross-aggregate communication
