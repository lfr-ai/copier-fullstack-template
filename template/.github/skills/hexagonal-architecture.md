# Skill: Clean / Hexagonal Architecture

## Purpose

Keep all backend changes compliant with clean / hexagonal architecture rules and the
Dependency Rule. Application services access persistence via UoW repository properties
(e.g. `uow.users`), never by importing concrete adapter classes.

## Use This Skill When

- Creating or moving backend modules
- Reviewing imports/dependencies across layers
- Splitting business logic from adapters/ports

## Rules

- Dependency direction must flow inward: `adapters/ports -> application -> core`
- `core/` has zero framework imports
- `application/` imports from `core/` only
- Business logic stays out of adapters, ports, and infrastructure
- No circular imports

## Quick Checklist

- [ ] File placed in correct layer
- [ ] Imports respect layer boundaries
- [ ] No framework types leaked into domain
- [ ] Domain entities remain pure dataclasses/value objects
