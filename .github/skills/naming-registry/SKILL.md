# Naming Registry Skill

## Overview

The naming registry is the single source of truth for ALL field names, column names,
API field names, and aliases used across the entire stack (Python ORM, Pydantic models,
TypeScript frontend).

## Registry Files

| File | Role | Editable? |
|------|------|-----------|
| `registry/naming_registry.json` | Source of truth | YES — edit this |
| `backend/src/claim_handler/core/registry_constants.py` | Generated Python constants | NO — auto-generated |
| `frontend/src/config/registry.ts` | Generated TypeScript constants | NO — auto-generated |
| `registry/generate_registry.py` | Code generator script | YES — maintain this |

## Workflow: Adding a New Field

1. Edit `registry/naming_registry.json` — add the field definition
2. Run `task generate-registry` to regenerate constants
3. Import the constant from `registry_constants.py` in Python code
4. Import from `registry.ts` in TypeScript code
5. NEVER hardcode the field name as a string literal

## Usage Patterns

### Python — ORM Column Names

```python
from claim_handler.core.registry_constants import ORM

class Claim(ORMBase):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        ORM.Claim.id,
        Integer,
        primary_key=True,
    )
```

### Python — Pydantic Aliases

```python
from claim_handler.core.registry_constants import Pydantic, APIFields

class ClaimModel(BaseModel):
    id: Annotated[
        int | None,
        Field(
            default=None,
            validation_alias=AliasChoices(Pydantic.Claim.id, APIFields.claims.id),
            serialization_alias=Pydantic.Claim.id,
            description="Unique claim identifier",
            examples=[1, 42],
        ),
    ]
```

### Python — API Field Names

```python
from claim_handler.core.registry_constants import APIFields

form_data.get(APIFields.claims.diagnosis)
```

### TypeScript — Frontend

```typescript
import { Routes, StatusText } from "../config/registry";

const url = Routes.cases.orchestrateCase();
```

## Rules

- NEVER hardcode field names as string literals
- NEVER hand-edit generated files (`registry_constants.py`, `registry.ts`)
- ALWAYS run generator after editing `naming_registry.json`
- ALWAYS import from registry constants, never from the JSON directly
- Maintain consistency: ORM name = Pydantic alias = API field name (unless explicit mapping)
