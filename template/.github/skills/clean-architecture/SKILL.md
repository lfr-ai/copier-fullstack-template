# Clean Architecture Skill

## Layer Hierarchy

```text
utils/ → config/ → core/ → infrastructure/ → ai/ → application/ → presentation/
```

Inner layers have ZERO knowledge of outer layers.
Outer layers depend on inner layers through imports.

## Dependency Rule

The fundamental invariant: **source-code dependencies always point inward**.

| Layer | Location | Responsibility | Dependencies |
|-------|----------|---------------|-------------|
| `utils/` | `backend/src/claim_handler/utils/` | Enums, validators, types, retry policies | stdlib only |
| `config/` | `backend/src/claim_handler/config/` | Frozen dataclass configurations | `utils/` |
| `core/` | `backend/src/claim_handler/core/` | ORM models, Pydantic models, registry | `utils/`, `config/` |
| `infrastructure/` | `backend/src/claim_handler/infrastructure/` | Azure OpenAI, external API clients | `config/`, `utils/`, `core/` |
| `ai/` | `backend/src/claim_handler/ai/` | RAG pipeline, embeddings, LangGraph | `config/`, `utils/`, `core/` |
| `application/` | `backend/src/claim_handler/application/` | Use cases, orchestration, services | `ai/`, `infrastructure/`, `core/`, `config/`, `utils/` |
| `presentation/` | `backend/src/claim_handler/presentation/` | FastAPI routes, middleware, DI | ALL layers |

## Boundary Rules

### Config Layer
- ALL config objects: `@dataclass(frozen=True, slots=True)`
- Config values from Azure Key Vault or environment variables
- Never hardcode connection strings or secrets

### Core Layer
- ORM: SQLAlchemy 2.0+ with `Mapped` and `mapped_column`
- Pydantic: `Annotated[type, Field(...)]` with `description` and `examples`
- Registry: `registry_constants.py` generated from `registry/naming_registry.json`
- Never hardcode field names — always use registry constants

### DI Wiring
- `presentation/api/dependencies.py` is the SINGLE wiring point
- Application services receive dependencies through constructor injection
- Never instantiate services directly in route handlers

## Adding a New Layer Component

1. Create module in the correct layer directory
2. Import only from allowed layers (see table above)
3. Add type hints, docstrings, and registry constants
4. Wire dependencies in `dependencies.py` if needed
5. Create tests in `tests/unit/` mirroring source structure

## Common Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Outward import | `utils/` imports from `application/` | Move shared code to `utils/` |
| Circular import | A ↔ B | Extract shared interface to lower layer |
| Hardcoded DI | `service = MyService()` in route | Use `Depends()` from `dependencies.py` |
| Mutable config | `@dataclass` without `frozen=True` | Add `frozen=True, slots=True` |
| Hardcoded names | `"claim_id"` string literal | Use `ORM.Claim.id` from registry |
