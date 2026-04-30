---
description: 'Create a new API endpoint with schema validation, tests, and documentation'
name: 'new-endpoint'
argument-hint: 'HTTP method + path + description (e.g., POST /api/users create user)'
agent: 'agent'
model: 'Claude Sonnet 4'
tools:
  [
    search/codebase,
    search/fileSearch,
    search/textSearch,
    search/usages,
    read/readFile,
    edit/editFiles,
    execute/runInTerminal,
    context7/get-library-docs,
    context7/resolve-library-id,
  ]
---

# New API Endpoint

Create a new API endpoint following project conventions.

## Steps

1. **Schema** — Create Pydantic request/response models in `presentation/api/schemas/`
2. **Service** — Add business logic in `application/services/`
3. **Route** — Register the endpoint in the appropriate router under `presentation/api/routes/`
4. **Tests** — Write unit and integration tests
5. **Verify** — Run linting, type checking, and tests

## Conventions

- Use `from __future__ import annotations`
- Use `Annotated[T, ...]` for dependency injection
- Use FastAPI status constants (e.g., `status.HTTP_201_CREATED`)
- Add OpenAPI description via docstrings
- All route handlers use keyword-only args
- Return typed response models, never raw dicts

## Verification

```bash
task backend:lint && task backend:typecheck && task backend:test:unit
```
