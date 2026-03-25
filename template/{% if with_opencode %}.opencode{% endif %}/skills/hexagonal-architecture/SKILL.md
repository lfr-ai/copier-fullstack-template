---
name: hexagonal-architecture
description:
  Enforces clean / hexagonal architecture (ports and adapters) rules for Python backend
  development — validates the Dependency Rule, layer boundaries, import restrictions,
  correct placement of business logic, and proper use of the UoW-with-repositories
  pattern
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: architecture
  layer: backend
---

## What I do

- Enforce clean / hexagonal architecture layer boundaries in Python backend code
- Validate the **Dependency Rule** (source-code dependencies always point inward)
- Ensure application services depend only on core protocols, never concrete adapters
- Verify the UoW-with-repositories pattern (services use `uow.users`, not direct adapter
  imports)
- Flag violations of layer isolation rules
- Suggest correct placement for new code

## Architecture Layers

```
core/           → Pure domain. ZERO external imports. Only stdlib + typing.
                  Defines interface protocols (ports) that adapters implement.
application/    → Use cases, services, DTOs. Imports from core only.
                  Access repos via UoW properties (uow.users). NO adapter imports.
ports/          → API routes, CLI, webhooks, DI container. FastAPI/Click allowed.
                  Wires concrete adapters into services.
adapters/       → DB repos, cache, HTTP clients. Implements core interface protocols.
                  Concrete UoW exposes typed repository properties.
infrastructure/ → DB engines, HTTP clients, security primitives, profiling (pyinstrument, tracemalloc, SQLAlchemy hooks)
utils/          → Shared leaf. stdlib + third-party only. NO first-party imports
config/         → Separate pillar. Settings, constants
```

## Mapping to Clean Architecture Circles

| Clean Architecture Circle    | Project Layer  | Directory         |
| ---------------------------- | -------------- | ----------------- |
| Enterprise Business Rules    | Core           | `core/`           |
| Application Business Rules   | Application    | `application/`    |
| Interface Adapters (driving) | Ports          | `ports/`          |
| Interface Adapters (driven)  | Adapters       | `adapters/`       |
| Frameworks & Drivers         | Infrastructure | `infrastructure/` |

## Rules I Enforce

### The Dependency Rule (Clean Architecture)

Source-code dependencies **always** point inward. An inner layer MUST NEVER import from
an outer layer:

```
adapters → ports → application → core
              ↑
        infrastructure
```

### UoW-with-Repositories Pattern

Application services receive a `UnitOfWork` protocol from core. The concrete UoW (in
adapters) exposes typed repository properties:

```python
# CORRECT: application service
async with self._uow as uow:
    user = await uow.users.get_by_id(user_id)

# INCORRECT: application service importing concrete adapter
from adapters.persistence.repositories.user_repository import UserRepository
repo = UserRepository(session=uow.session)
```

### Strict Prohibitions

- NO business logic in adapters, ports, infrastructure, or middleware
- NO ORM models in core — use pure dataclasses (frozen=True, slots=True)
- NO Pydantic models in core — Pydantic is a port/adapter concern
- NO adapter imports in application layer (Dependency Rule violation)
- NO concrete repository instantiation in application services
- NO circular dependencies between any modules
- NO relative imports except within `__init__.py`
- NO framework imports in core or application layers

## When to use me

Use this skill when:

- Creating new modules or files
- Moving code between layers
- Adding new repositories or services
- Reviewing architecture compliance
- Planning structural changes
- Verifying the Dependency Rule after refactoring
