# Core

Pure domain logic — **no framework dependencies**.

**Rules:**

- No Pydantic, no SQLAlchemy, no FastAPI, no httpx.
- Only stdlib, `typing`, and intra-`core` imports allowed.
- Entities are mutable dataclasses with `slots=True` (need mutable `_events`).
- Aggregate roots (`AggregateRoot`) extend `Entity` and mark the consistency boundary
  for a cluster of objects. Repositories only reference aggregate roots.
- Value objects are immutable (`frozen=True, slots=True`).
- Interfaces (protocols) define contracts for adapters — these are the **ports** in
  Ports & Adapters terminology.
- Domain services contain cross-entity business rules that don't belong in a single
  entity.
- Specifications encapsulate reusable business predicates.
- Exceptions are domain-specific.
- Events represent things that happened in the domain.

| Package            | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `domain_services/` | Cross-entity business rules (stateless domain logic)            |
| `entities/`        | Domain entities and aggregate roots (`slots=True`)              |
| `enums/`           | Domain enumerations                                             |
| `events/`          | Domain events                                                   |
| `exceptions/`      | Domain-specific exception hierarchy                             |
| `interfaces/`      | Port protocols — contracts for driven adapters and repositories |
| `specifications/`  | Composable business rule predicates (Specification pattern)     |
| `value_objects/`   | Immutable value types (Email, EmbeddingConfig)                  |
| `types.py`         | NewType aliases for domain IDs                                  |
