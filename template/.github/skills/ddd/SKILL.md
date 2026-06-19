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

Objects with identity that persists over time. Located in `core/entities/`.

### 2. Value Objects

Immutable objects defined by their attributes, not identity. Located in `core/value_objects/`.

### 3. Aggregates

Cluster of domain objects treated as a unit for consistency.

### 4. Ports (Interfaces)

Abstract protocols defining contracts between layers. Located in `core/interfaces/`.

## Clean Architecture Mapping

| DDD Concept | Location | Example |
|------------|----------|---------|
| Entity | `core/entities/` | `User`, `Order` |
| Value Object | `core/value_objects/` | `Email`, `Money` |
| Repository Protocol | `core/interfaces/` | `IUserRepository` |
| Domain Event | `core/events/` | `OrderPlaced` |
| Application Service | `application/services/` | `CreateOrderService` |
