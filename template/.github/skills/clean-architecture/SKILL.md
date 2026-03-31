---
name: clean-architecture
description: >
    Enforces Clean Architecture boundaries and the Dependency Rule.
    Use when creating or moving backend modules, reviewing imports, or splitting
    business logic from infrastructure and presentation layers.
---

# Skill: Clean Architecture

## Purpose

Keep all backend changes compliant with Clean Architecture rules and the
Dependency Rule. Application services access persistence via UnitOfWork repository properties
(e.g. `uow.users`), never by importing concrete infrastructure classes.

## Use This Skill When

- Creating or moving backend modules
- Reviewing imports/dependencies across layers
- Splitting business logic from infrastructure/presentation layers

## Rules

- Dependency direction must flow inward: `presentation/infrastructure -> application -> core`
- `core/` has zero framework imports
- `application/` imports from `core/` only (domain entities, protocols, exceptions)
- Business logic stays out of infrastructure and presentation layers
- No circular imports
- Presentation and Infrastructure never depend on each other

## Quick Checklist

- [ ] File placed in correct layer (core/application/infrastructure/presentation)
- [ ] Imports respect layer boundaries (dependencies point inward)
- [ ] No framework types leaked into domain core
- [ ] Domain entities remain pure dataclasses/value objects
- [ ] Infrastructure implementations use Gateway/Repository protocols from core
