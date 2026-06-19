---
name: ddd
description: "Domain-Driven Design tactical patterns for the domain layer. Use when designing entities, value objects, aggregates, or reviewing domain model compliance."
---

# Domain-Driven Design (DDD) Skill

Tactical DDD patterns for the domain layer (`core/`).

## When to Use This Skill

- Designing new domain concepts (entities, value objects, aggregates)
- Reviewing domain model for DDD compliance
- Identifying aggregate boundaries
- Extracting value objects from primitives
- Modeling domain events
- Creating repository protocols

## DDD Tactical Patterns

### 1. Entities

**Definition**: Objects with identity that persists over time.

### 2. Value Objects

**Definition**: Immutable objects defined by their attributes, not identity.

### 3. Aggregates

**Definition**: Cluster of domain objects treated as a unit for consistency.

### 4. Ports (Interfaces)

**Definition**: Abstract protocols defining contracts between layers.

## Clean Architecture Mapping

| DDD Concept | Location | Example |
|------------|----------|---------|
| Entity | `core/entities/` | `User`, `Document` |
| Value Object | `core/value_objects/` | `Email`, `CPR` |
| Port | `core/interfaces/` | `UserRepository`, `LLMGateway` |
| Domain Service | `core/domain_services/` | `PasswordPolicy` |
| Application Service | `application/services/` | `UserService` |
| Repository Impl | `infrastructure/persistence/repositories/` | `SQLAlchemyUserRepository` |
