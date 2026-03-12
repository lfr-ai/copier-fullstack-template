
Pure domain logic. **ZERO external imports** — only stdlib and `typing`.

**Rules:**

- No Pydantic, no SQLAlchemy, no FastAPI, no httpx — nothing outside stdlib.
- Entities are mutable dataclasses with `slots=True` (need mutable `_events`).
- Value objects are immutable (`frozen=True, slots=True`).
- Interfaces (protocols) define contracts for adapters.
- Exceptions are domain-specific.
- Events represent things that happened in the domain.


| Package           | Purpose                                                 |
| ----------------- | ------------------------------------------------------- |
| `entities/`       | Domain entities (mutable dataclasses with `slots=True`) |
| `enums/`          | Domain enumerations                                     |
| `events/`         | Domain events                                           |
| `exceptions/`     | Domain-specific exception hierarchy                     |
| `interfaces/`     | Repository and service protocols                        |
| `specifications/` | Specification pattern for queries                       |
| `value_objects/`  | Immutable value types (Email, Money)                    |
| `types.py`        | NewType aliases for domain IDs                          |
