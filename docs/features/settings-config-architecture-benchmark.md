# Feature: settings/config architecture benchmark (koda_refactor)

## Purpose and scope

Document a deep comparative review between `koda_refactor` and
`copier-fullstack-template` focused on:

- settings/config module structure,
- runtime environment resolution strategy,
- environment-class design and naming,
- validator reuse and testability.

This feature also records concrete scaffold changes implemented in this pass.

## Analyzed files

### External reference (`koda_refactor`)

- `src/koda/configs/base.py`
- `src/koda/configs/runtime.py`
- `src/koda/configs/_validators.py`
- `src/koda/configs/environments/{local,dev,test,staging,prod}.py`
- `src/koda/composition/container.py`
- `src/koda/presentation/api/dependency_registry.py`

### Template repository

- `template/backend/src/{{ project_slug }}/config/settings/base.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/runtime.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/{local,dev,test,staging,prod}.py.jinja`
- `template/backend/tests/unit/config/test_settings.py.jinja`
- `template/backend/tests/unit/config/test_runtime.py.jinja` (added)

## Architectural findings

### Strengths already present in template

- Clear per-environment classes with safe production defaults.
- Deterministic runtime environment precedence (`process -> env files -> hostname`).
- Cached settings factory (`lru_cache`) and strict prod/staging secret checks.

### Gaps observed against benchmark

- Validation logic was centralized in one large model validator and duplicated in
  environment subclasses.
- No dedicated validator helper module to isolate business-rule validation concerns.
- Settings tests had stale expectations for environment-class mapping and lacked
  runtime precedence regression coverage.

## Implemented changes

1. Added reusable validator module:
   - `template/backend/src/{{ project_slug }}/config/settings/_validators.py.jinja`
   - Provides `validate_secret_key_strength()` and
     `validate_auth_configuration()`.

2. Refactored settings classes to use reusable validators:
   - `base.py.jinja`: now delegates auth and secret validation to helper module.
   - `staging.py.jinja` and `prod.py.jinja`: replaced duplicated secret-key logic
     with shared validator.

3. Upgraded settings tests for correctness and regression safety:
   - `test_settings.py.jinja`:
     - fixed stale class expectations (`DEV -> DevSettings`,
       `STAGING -> StagingSettings`),
     - isolated `get_settings()` cache across tests,
     - added strict secret validation coverage for prod/staging,
     - aligned test-environment debug expectation to current behavior.
   - `test_runtime.py.jinja` (new):
     - validates runtime precedence and fallback behavior,
     - validates `get_settings()` cache behavior.

## Business rules and constraints

- Configuration validation must remain deterministic and environment-aware.
- Security-sensitive defaults must fail fast outside local development.
- Validation logic should be reusable and testable in isolation.
- Changes must preserve Clean Architecture boundaries.

## Security and operational impact

- Strengthens auth-configuration safety with explicit JWT configuration checks.
- Keeps production/staging secret requirements centralized and consistent.
- Reduces configuration drift risk via improved unit-test coverage.
