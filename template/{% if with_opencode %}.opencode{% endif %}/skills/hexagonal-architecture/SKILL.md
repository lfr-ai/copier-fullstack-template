---
name: hexagonal-architecture
description: Enforces hexagonal (ports and adapters) architecture rules for Python backend development
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: architecture
---

## What I do

- Enforce hexagonal architecture layer boundaries in Python backend code
- Validate dependency direction (always inward)
- Flag violations of layer isolation rules
- Suggest correct placement for new code

## Architecture Layers

```
core/        → Pure domain. ZERO external imports. Only stdlib + typing
application/ → Use cases, services, DTOs. Imports from core only
ports/       → API routes, CLI, webhooks. FastAPI/Typer allowed
adapters/    → DB repos, cache, HTTP clients. Implements core interfaces
infrastructure/ → DB engines, HTTP clients, security primitives
utils/       → Shared leaf. stdlib + third-party only. NO first-party imports
config/      → Separate pillar. Settings, constants
```

## Rules I Enforce

### Dependency Direction
```
adapters → ports → application → core
              ↑
        infrastructure
```

### Strict Prohibitions
- NO business logic in adapters, ports, infrastructure, or middleware
- NO ORM models in core — use pure dataclasses (frozen=True, slots=True)
- NO Pydantic models in core — Pydantic is a port/adapter concern
- NO circular dependencies between any modules
- NO relative imports except within __init__.py
- NO framework imports in core or application layers

## When to use me

Use this skill when:
- Creating new modules or files
- Moving code between layers
- Reviewing architecture compliance
- Planning structural changes
