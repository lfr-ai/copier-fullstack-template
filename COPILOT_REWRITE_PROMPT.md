# Comprehensive GitHub Copilot Prompt — Copier Fullstack Template Rewrite

> **Purpose**: This is an exhaustive, self-contained prompt for GitHub Copilot (or any AI coding agent) to rewrite the `copier-fullstack-template` Copier project template. It encodes every architectural decision, file, pattern, naming convention, and design constraint derived from a deep analysis of the existing codebase plus the reference `claim_handler` project.

---

## 0. META — What This Template Is

This is a **Copier 9+** project template (`copier.yml` + `template/` directory with `.jinja` suffixed files) that scaffolds a production-ready **fullstack Python + TypeScript** application. When a user runs `uvx copier copy --trust . ../my_project`, Copier prompts for variables and renders every `.jinja` file, producing a complete, working, opinionated project. The template itself lives in its own Git repo and is never deployed — only the _rendered output_ is a real application.

---

## 1. COPIER CONFIGURATION (`copier.yml`) — COMPLETE SPECIFICATION

Rewrite `copier.yml` with exactly these sections and variables. Remove ALL references to AWS, GCP, SQLite. Add `frontend_framework` and `with_opencode`. Ensure conditional `when:` guards are correct.

```yaml
_min_copier_version: "9.0.0"
_subdirectory: "template"
_templates_suffix: ".jinja"

_exclude:
  - "copier.yml"
  - "copier.yaml"
  - "~*"
  - "*.py[co]"
  - "__pycache__"
  - ".git"
  - ".DS_Store"
  - ".svn"

_skip_if_exists:
  - ".env"
  - ".env.dev"
  - ".env.prod"
  - ".env.test"
  - "CHANGELOG.md"
  - "backend/seeds/initial_data.json"
```

### 1.1. Project Metadata Variables

| Variable              | Type  | Default                                                               | Validation                     | Notes                            |
| --------------------- | ----- | --------------------------------------------------------------------- | ------------------------------ | -------------------------------- |
| `project_name`        | `str` | —                                                                     | Required, non-empty            | Human-readable display name      |
| `project_slug`        | `str` | `{{ project_name \| lower \| replace(' ','_') \| replace('-','_') }}` | Must match `^[a-z][a-z0-9_]*$` | Python package name (snake_case) |
| `project_description` | `str` | `"A fullstack Python application"`                                    | —                              | Short one-liner                  |
| `author_name`         | `str` | —                                                                     | Required                       | —                                |
| `author_email`        | `str` | —                                                                     | Must match `.+@.+\..+`         | —                                |
| `github_username`     | `str` | `{{ author_name \| lower \| replace(' ','-') }}`                      | —                              | GitHub user/org                  |
| `copyright_year`      | `str` | `{{ '%Y' \| strftime }}`                                              | —                              | —                                |

### 1.2. Technical Choices Variables

| Variable             | Type  | Default  | Choices                                                                              | Notes                     |
| -------------------- | ----- | -------- | ------------------------------------------------------------------------------------ | ------------------------- |
| `python_version`     | `str` | `"3.13"` | `"3.12"`, `"3.13"`                                                                   | Minimum Python            |
| `node_version`       | `str` | `"22"`   | `"20"`, `"22"`                                                                       | Node.js major version     |
| `frontend_framework` | `str` | `"lit"`  | `Lit (lightweight Web Components + Vite): "lit"`, `React (React 19 + Vite): "react"` | Frontend framework choice |

### 1.3. Database Variables

| Variable           | Type  | Default        | Choices                                                                                                                                         | Condition                                                                                                                                                 |
| ------------------ | ----- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `database_backend` | `str` | `"postgresql"` | `None (no database): "none"`, `PostgreSQL (local container): "postgresql"`, `Azure Database for PostgreSQL Flexible Server: "azure_postgresql"` | `when: "{{ cloud_provider == 'none' or cloud_provider == 'azure' }}"`. The `azure_postgresql` choice should only appear when `cloud_provider == 'azure'`. |

**When `database_backend == "postgresql"`**: Set up a local PostgreSQL container in compose, include psycopg + asyncpg dependencies, configure Alembic, create DB healthchecks, include DB seed scripts, and create backup scripts.

**When `database_backend == "azure_postgresql"`**: In addition to the above, add a Bicep module `modules/postgres.bicep` for Azure Database for PostgreSQL Flexible Server, add connection string configuration via Azure Key Vault or env vars.

**When `database_backend == "none"`**: Exclude all database containers, remove SQLAlchemy/Alembic/psycopg dependencies, stub the repository with in-memory implementations, remove migration tasks/scripts.

### 1.4. Feature Flags Variables

| Variable            | Type   | Default    | Notes                                              |
| ------------------- | ------ | ---------- | -------------------------------------------------- |
| `use_celery`        | `bool` | `true`     | Requires Redis                                     |
| `use_redis`         | `bool` | `true`     | Cache + message broker                             |
| `use_caddy`         | `bool` | `true`     | Reverse proxy (TLS, compression, security headers) |
| `use_auth`          | `bool` | `true`     | JWT + session authentication                       |
| `use_playwright`    | `bool` | `true`     | E2E browser tests                                  |
| `use_devcontainer`  | `bool` | `true`     | VS Code devcontainer config                        |
| `with_opencode`     | `bool` | `false`    | OpenCode AI coding agent install script + config   |
| `container_runtime` | `str`  | `"podman"` | Choices: `"podman"`, `"docker"`                    |

### 1.5. Cloud & Infrastructure Variables

| Variable         | Type  | Default           | Choices                                                | Condition                                                                                                                                                |
| ---------------- | ----- | ----------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cloud_provider` | `str` | `"none"`          | `None (local only): "none"`, `Azure: "azure"`          | —                                                                                                                                                        |
| `azure_location` | `str` | `"swedencentral"` | —                                                      | `when: "{{ cloud_provider == 'azure' }}"`                                                                                                                |
| `secret_backend` | `str` | `"env"`           | `Env files only: "env"`, `Azure Key Vault: "azure_kv"` | `when: "{{ cloud_provider == 'azure' or cloud_provider == 'none' }}"`. The `azure_kv` choice should only be meaningful when `cloud_provider == 'azure'`. |

### 1.6. License Variable

| Variable  | Type  | Default | Choices                                               |
| --------- | ----- | ------- | ----------------------------------------------------- |
| `license` | `str` | `"MIT"` | `"MIT"`, `"Apache-2.0"`, `"GPL-3.0"`, `"Proprietary"` |

### 1.7. Post-Generation Tasks

```yaml
_tasks:
  - command: "git init"
    when: "{{ _copier_operation == 'copy' }}"
  - command: "git add ."
    when: "{{ _copier_operation == 'copy' }}"
  - command: "git commit -m 'feat: initial scaffold from copier-fullstack-template'"
    when: "{{ _copier_operation == 'copy' }}"
```

Keep the existing `_message_after_copy` and `_message_after_update` banners.

---

## 2. ARCHITECTURE — HEXAGONAL / CLEAN ARCHITECTURE (MANDATORY)

The backend **MUST** follow hexagonal architecture (ports and adapters) with strict inward-only dependency flow:

```
┌─────────────────────────────────────────┐
│  Ports (API routes, CLI, webhooks)      │  ← Framework-specific entry points
├─────────────────────────────────────────┤
│  Application (services, commands, DTOs) │  ← Orchestration, use cases
├─────────────────────────────────────────┤
│  Core (entities, value objects, events) │  ← Pure domain, ZERO framework imports
├─────────────────────────────────────────┤
│  Adapters (DB, cache, HTTP, email)      │  ← External integration implementations
├─────────────────────────────────────────┤
│  Infrastructure (engines, clients)      │  ← Low-level technical concerns
└─────────────────────────────────────────┘
```

### 2.1. Layer Import Rules (ENFORCED)

- **Core** imports NOTHING external. Only `stdlib`, `typing`, `collections.abc`, `dataclasses`, `enum`, `uuid`, `datetime`, `decimal`, `re`.
- **Application** imports from `core` only. No framework imports (no FastAPI, no SQLAlchemy, no Pydantic).
- **Ports** imports from `application` and `core`. FastAPI/Typer/Click/Pydantic allowed here.
- **Adapters** imports from all inner layers. SQLAlchemy, httpx, redis, etc. allowed here.
- **Infrastructure** provides low-level primitives (DB engines, HTTP clients, security). May import third-party.
- **Utils** is a shared leaf — `stdlib` + third-party only. NO first-party imports.
- **Config** is a separate pillar — settings, constants, logging. Not part of the layer stack.

### 2.2. Mandatory Coding Rules

- `from __future__ import annotations` in **every** Python file
- All `__init__.py` MUST define `__all__`
- Keyword-only arguments: all constructors and multi-param functions use `*`
- NO `print()` — use `structlog`
- NO `Any` type — use proper generics or `Unknown`
- NO mutable default arguments
- NO `assert` for runtime validation
- NO relative imports except within `__init__.py`
- NO f-strings in logging calls — use `%s` formatting
- Exception chaining: `raise NewError(...) from original_error`
- Use `pathlib.Path` over `os.path`
- Use `datetime.UTC` for timezone-aware datetimes
- Use `decimal.Decimal` for monetary values
- Use `collections.abc` over `typing` for generic collection types
- Constants: `Final` type annotation
- Google-style docstrings on all public modules, classes, functions, methods
- Line length: 99 characters
- Python 3.12+ syntax: `type` statements, `X | Y` unions, `match` expressions, PEP 695 generics

### 2.3. Design Patterns (ALL must be implemented)

| Pattern              | Location                                                                 | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **CQRS**             | `application/commands/`, `application/queries/`                          | `CommandHandler[CommandT, ResultT]` + `QueryHandler[QueryT, ResultT]` abstract base classes |
| **Repository**       | `core/interfaces/repository.py` → `adapters/persistence/repositories/`   | Generic `Repository[EntityT]` protocol → `SQLAlchemyRepository[ModelT]`                     |
| **Unit of Work**     | `core/interfaces/unit_of_work.py` → `adapters/persistence/unit_of_work/` | `UnitOfWork` protocol → `SQLAlchemyUnitOfWork` async context manager                        |
| **Domain Events**    | `core/events/` → `adapters/messaging/`                                   | `DomainEvent` base → `EventBus` protocol → `MemoryEventBus`                                 |
| **Value Objects**    | `core/value_objects/`                                                    | Frozen dataclasses with `__post_init__` validation (e.g., `Email`)                          |
| **Entity Base**      | `core/entities/base.py`                                                  | UUID identity, event collection, equality-by-ID                                             |
| **Specification**    | `core/specifications/`                                                   | Placeholder package for future specification pattern                                        |
| **DI Container**     | `ports/container.py`                                                     | Manual `Container` class with `@lru_cache` singleton accessors                              |
| **Factory Method**   | `ports/api/app.py`, `config/celery.py`                                   | `create_api_app()`, `create_celery_app()`                                                   |
| **DTO**              | `application/dtos/`                                                      | Pydantic-free DTOs (frozen dataclasses) for inter-layer communication                       |
| **Mapper**           | `application/mappers/`                                                   | Entity ↔ DTO mapping                                                                        |
| **Strategy**         | `config/settings/`                                                       | Environment-specific settings: `LocalSettings`, `ProdSettings`, `TestSettings`              |
| **Retry/Resilience** | `utils/retry_policies.py`                                                | Tenacity decorators with exponential backoff                                                |

### 2.4. Known Issues to Fix

These bugs exist in the current codebase and MUST be fixed in the rewrite:

1. **Session inconsistency in DI Container**: `container.py` creates a session for `UserRepository` and a _separate_ session for `SQLAlchemyUnitOfWork`. The repository and UoW must share the same session. Fix: inject the UoW's session factory into repositories, not a pre-created session.

2. **API routes bypass schema layer**: `users.py` routes use `CreateUserDTO` (application layer) directly as request body instead of the `CreateUserRequest` schema (ports layer). Fix: use API schemas at the route boundary and map to DTOs in the route handler.

3. **Dual pagination mismatch**: `application/dtos/pagination.py` uses `offset/limit` while `ports/api/schemas/pagination.py` uses `page/page_size`. Fix: align both or add an explicit mapper.

4. **SmtpEmailAdapter blocks event loop**: The `send()` method is `async` but uses synchronous `smtplib.SMTP`. Fix: run in `asyncio.to_thread()`.

5. **Missing protocols for Email and Storage**: `CachePort` and `EventBus` have core protocols but `EmailPort` and `StoragePort` do not. Fix: add `core/interfaces/email.py` and `core/interfaces/storage.py` with Protocol definitions.

6. **Health routes return raw dicts**: The `HealthResponse` Pydantic schema exists but health routes return plain dicts. Fix: return `HealthResponse` instances.

7. **`BaseService[ResultT]` is vestigial**: The type parameter is unused. Fix: either use it properly (e.g., as the return type of an abstract method) or remove the generic parameter.

8. **Jinja template indentation issues**: Several conditionally-included files (celery.py, redis.py, jwt_adapter.py, example_tasks.py) lose indentation inside `{% if %}` blocks. Fix: ensure all code inside conditional blocks retains proper Python indentation.

---

## 3. BACKEND — COMPLETE FILE TREE AND SPECIFICATION

**Language**: Python only (extensible later). **Framework**: FastAPI + Uvicorn. **ORM**: SQLAlchemy 2.0 async. **Migrations**: Alembic.

### 3.1. Complete Backend Source Tree

```
backend/
├── alembic.ini.jinja
├── pyproject.toml.jinja
├── tox.ini.jinja
├── alembic/
│   ├── env.py.jinja
│   └── versions/.gitkeep
├── seeds/
│   └── initial_data.json
├── tools/
│   ├── dependency_graph.py
│   ├── generate_migration.py
│   ├── analysis/.gitkeep
│   ├── generators/.gitkeep
│   └── hooks/.gitkeep
├── src/{{ project_slug }}/
│   ├── __init__.py.jinja          # Package version + __all__
│   ├── __main__.py.jinja          # `python -m {{ project_slug }}` entry
│   ├── main.py.jinja              # FastAPI app factory import
│   ├── py.typed                   # PEP 561 marker
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py           # App-level constants (TOKEN_EXPIRY, RATE_LIMITS, etc.)
│   │   ├── logging.py.jinja       # structlog configuration (JSON prod, console dev)
│   │   ├── README.md
│   │   ├── {% if use_celery %}celery.py{% endif %}.jinja
│   │   ├── {% if use_redis %}redis.py{% endif %}.jinja
│   │   └── settings/
│   │       ├── __init__.py.jinja  # `get_settings()` factory dispatching on environment enum
│   │       ├── base.py.jinja      # BaseSettings (pydantic-settings) with all env vars
│   │       ├── local.py.jinja     # LocalSettings overrides (DEBUG=True, etc.)
│   │       ├── prod.py.jinja
│   │       └── test.py.jinja
│   ├── core/
│   │   ├── __init__.py
│   │   ├── constants.py           # Domain constants (MAX_EMAIL_LENGTH, etc.)
│   │   ├── types.py               # Type aliases (EntityId = UUID, etc.)
│   │   ├── README.md
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Entity base class (UUID id, events, eq-by-id)
│   │   │   └── user.py.jinja
│   │   ├── enums/
│   │   │   ├── __init__.py        # Barrel export
│   │   │   ├── base.py            # ParseableEnum(StrEnum) with from_str()
│   │   │   ├── environment.py     # Environment enum (local, test, staging, prod)
│   │   │   ├── service_status.py  # ServiceStatus (healthy, degraded, unhealthy)
│   │   │   ├── sort_order.py      # SortOrder (asc, desc)
│   │   │   └── status.py          # Status (active, inactive, suspended, deleted)
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   └── user_events.py.jinja  # UserCreated, UserUpdated, etc. (frozen dataclasses)
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # BaseAppError hierarchy (NotFoundError, ValidationError, etc.)
│   │   │   └── validation.py.jinja
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   ├── cache.py           # CachePort protocol
│   │   │   ├── email.py           # EmailPort protocol ← NEW (fix missing protocol)
│   │   │   ├── event_bus.py.jinja # EventBus protocol
│   │   │   ├── repository.py.jinja # Repository[EntityT] protocol
│   │   │   ├── storage.py         # StoragePort protocol ← NEW (fix missing protocol)
│   │   │   └── unit_of_work.py    # UnitOfWork protocol
│   │   ├── specifications/
│   │   │   └── __init__.py        # Placeholder for specification pattern
│   │   └── value_objects/
│   │       ├── __init__.py
│   │       └── email.py.jinja     # Email value object (frozen dataclass, validated)
│   ├── application/
│   │   ├── __init__.py
│   │   ├── interfaces.py          # Application-level service protocols
│   │   ├── README.md
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   └── base.py.jinja      # CommandHandler[CommandT, ResultT] ABC
│   │   ├── dtos/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # BaseDTO (frozen dataclass)
│   │   │   ├── pagination.py.jinja # PaginationDTO — use page/page_size (align with API)
│   │   │   └── user_dto.py.jinja
│   │   ├── mappers/
│   │   │   ├── __init__.py
│   │   │   └── user_mapper.py.jinja
│   │   ├── queries/
│   │   │   ├── __init__.py
│   │   │   └── base.py            # QueryHandler[QueryT, ResultT] ABC
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── base.py.jinja      # BaseService (fix: remove vestigial generic or use it)
│   │   │   └── user_service.py.jinja # Fix: use UoW session, not separate sessions
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── {% if use_celery %}example_tasks.py{% endif %}.jinja
│   │   └── validators/
│   │       └── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── {% if use_auth %}auth{% endif %}/
│   │   │   ├── {% if use_auth %}__init__.py{% endif %}
│   │   │   └── {% if use_auth %}jwt_adapter.py{% endif %}.jinja
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── memory_cache.py
│   │   │   └── {% if use_redis %}redis_cache.py{% endif %}
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── console_email_adapter.py
│   │   │   └── smtp_email_adapter.py.jinja  # Fix: use asyncio.to_thread()
│   │   ├── external/
│   │   │   ├── __init__.py
│   │   │   └── http_client.py.jinja
│   │   ├── messaging/
│   │   │   ├── __init__.py
│   │   │   └── memory_event_bus.py.jinja
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── session.py.jinja   # Async session factory
│   │   │   ├── mappers/__init__.py
│   │   │   ├── orm/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py        # SQLAlchemy declarative base
│   │   │   │   └── user_model.py.jinja
│   │   │   ├── repositories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py.jinja  # SQLAlchemyRepository[ModelT]
│   │   │   │   └── user_repository.py.jinja
│   │   │   └── unit_of_work/
│   │   │       ├── __init__.py
│   │   │       └── sqlalchemy_uow.py # Fix: share session with repositories
│   │   └── storage/
│   │       ├── __init__.py
│   │       ├── local_storage_adapter.py
│   │       └── azure_blob_storage_adapter.py  # CHANGED: was s3, now Azure Blob (when cloud_provider == 'azure')
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── container.py.jinja     # DI container — fix session sharing
│   │   ├── README.md
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── app.py.jinja       # create_api_app() factory with lifespan
│   │   │   ├── dependencies.py.jinja # FastAPI Depends() providers
│   │   │   ├── router.py.jinja    # Central router aggregation
│   │   │   ├── middleware/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── authentication.py
│   │   │   │   ├── authorization.py
│   │   │   │   ├── compression.py
│   │   │   │   ├── cors.py.jinja
│   │   │   │   ├── error_handler.py.jinja
│   │   │   │   ├── rate_limit.py
│   │   │   │   ├── request_id.py
│   │   │   │   ├── security_headers.py
│   │   │   │   └── timing.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py      # Fix: return HealthResponse, not raw dict
│   │   │   │   └── users.py.jinja # Fix: use API schemas, map to DTOs
│   │   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── error_response.py
│   │   │   │   ├── health.py.jinja
│   │   │   │   ├── pagination.py.jinja # Align with DTO pagination
│   │   │   │   ├── sorting.py.jinja
│   │   │   │   └── user_schema.py.jinja
│   │   │   └── v1/__init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── app.py.jinja       # Click CLI entry
│   │   │   ├── commands/__init__.py
│   │   │   └── utils/__init__.py
│   │   ├── gateways/__init__.py
│   │   └── web/
│   │       ├── __init__.py
│   │       ├── controllers/
│   │       │   ├── __init__.py
│   │       │   └── home.py.jinja
│   │       ├── forms/__init__.py
│   │       └── view_models/
│   │           ├── __init__.py
│   │           └── base.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── health.py
│   │   ├── scheduling/
│   │   │   ├── __init__.py
│   │   │   └── scheduler.py
│   │   └── security/
│   │       ├── __init__.py
│   │       └── hashing.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── README.md
│   │   ├── agents/__init__.py
│   │   ├── chains/__init__.py
│   │   ├── embeddings/__init__.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── azure_openai_adapter.py
│   │   │   ├── base_llm_adapter.py
│   │   │   └── openai_adapter.py
│   │   ├── models/__init__.py
│   │   ├── prompts/__init__.py
│   │   ├── providers/__init__.py
│   │   ├── services/__init__.py.jinja
│   │   └── tools/__init__.py
│   └── utils/
│       ├── __init__.py
│       ├── crypto_utils.py
│       ├── file_utils.py
│       ├── json_utils.py
│       ├── logger_factory.py
│       ├── pagination_utils.py
│       ├── README.md
│       ├── retry_policies.py
│       ├── string_utils.py.jinja
│       ├── timing.py
│       └── validators.py
└── tests/
    ├── __init__.py
    ├── conftest.py.jinja
    ├── factories/
    │   ├── __init__.py
    │   └── user_factory.py.jinja
    ├── fixtures/
    │   ├── __init__.py
    │   ├── cache.py.jinja
    │   └── database.py.jinja
    ├── mocks/__init__.py
    ├── utils/
    │   ├── __init__.py
    │   ├── assertion_helpers.py
    │   ├── fixture_factory.py
    │   └── mock_builder.py
    ├── integration/
    │   ├── __init__.py
    │   ├── test_api.py.jinja
    │   └── test_database.py.jinja
    ├── performance/
    │   ├── __init__.py
    │   └── .gitkeep
    ├── property/
    │   ├── __init__.py
    │   ├── test_generate_registry.py.jinja
    │   └── test_value_objects.py.jinja
    └── unit/
        ├── __init__.py
        ├── conftest.py.jinja
        ├── adapters/     # All adapter unit tests
        ├── ai/           # AI adapter unit tests
        ├── application/  # Service/command/query/mapper/DTO tests
        ├── config/       # Settings, logging, celery, redis config tests
        ├── core/         # Entity, enum, event, exception, VO tests
        ├── infrastructure/ # DB health, hashing, scheduler tests
        ├── ports/        # Route, schema, middleware, CLI tests
        └── utils/        # Utility function tests
```

### 3.2. `pyproject.toml.jinja` Specification

**Build system**: hatchling (`hatchling.build`)
**Package**: `src/{{ project_slug }}` layout
**Python**: `>={{ python_version }}`

#### Core Dependencies (always included)

```
fastapi>=0.115
uvicorn[standard]>=0.34
pydantic>=2.10
pydantic-settings>=2.7
jinja2>=3.1
httpx>=0.28
tenacity>=9.0
structlog>=24.4
slowapi>=0.1
click>=8.1
rich>=13.9
tqdm>=4.67
python-multipart>=0.0.18
```

#### Conditional dependencies

```python
# Database (when database_backend != "none")
{%- if database_backend != "none" %}
sqlalchemy[asyncio]>=2.0
alembic>=1.14
psycopg[binary]>=3.2      # PostgreSQL driver (sync)
asyncpg>=0.30              # PostgreSQL driver (async)
{%- endif %}

# Redis
{%- if use_redis %}
redis>=5.2
{%- endif %}

# Celery
{%- if use_celery %}
celery[redis]>=5.4
{%- endif %}

# Auth
{%- if use_auth %}
python-jose[cryptography]>=3.3
passlib[bcrypt]>=1.7
{%- endif %}

# Azure Key Vault (when secret_backend == "azure_kv")
{%- if secret_backend == "azure_kv" %}
azure-identity>=1.19
azure-keyvault-secrets>=4.9
{%- endif %}
```

**Remove**: boto3, google-cloud-secret-manager, aiosqlite (no AWS, GCP, SQLite).

#### Dev Dependencies (optional group `[dev]`)

```
pytest>=8.3
pytest-asyncio>=0.24
pytest-cov>=6.0
pytest-xdist>=3.5
pytest-mock>=3.14
hypothesis>=6.119
factory-boy>=3.3
freezegun>=1.4
respx>=0.22
ruff>=0.9
ty>=0.0
pre-commit>=4.0
tox>=4.23
tox-uv>=1.16
pip-audit>=2.7
detect-secrets>=1.5
```

#### Ruff Config (30+ rule categories)

```toml
[tool.ruff]
target-version = "py312"
line-length = 99
src = ["src"]

[tool.ruff.lint]
select = ["F","E","W","C90","I","N","UP","S","B","A","C4","DTZ","T10","T20","ISC","ICN","PIE","PT","Q","RSE","RET","SLF","SIM","TID","TCH","ARG","PTH","ERA","PL","TRY","FLY","PERF","FURB","LOG","RUF","ANN","D"]
ignore = ["D100","D104","D106","D203","D213","ANN101","ANN102","ANN401","S101","TRY003","EM101","EM102"]

[tool.ruff.lint.pydocstyle]
convention = "google"
```

#### Type Checking

```toml
[tool.ty]
python-version = "{{ python_version }}"
```

#### Coverage

```toml
[tool.coverage.run]
branch = true
source = ["{{ project_slug }}"]

[tool.coverage.report]
fail_under = 80
exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:", "@overload"]
```

#### CLI Entry Point

```toml
[project.scripts]
{{ project_slug }} = "{{ project_slug }}.ports.cli.app:main"
```

### 3.3. Storage Adapter — Azure Blob (Replace S3)

Replace `s3_storage_adapter.py` with `azure_blob_storage_adapter.py` (conditionally included when `cloud_provider == 'azure'`). Uses `azure-storage-blob` SDK. Must implement the `StoragePort` protocol from `core/interfaces/storage.py`.

---

## 4. FRONTEND — COMPLETE SPECIFICATION

### 4.1. Framework Choice (`frontend_framework`)

The template **MUST** support two frontend frameworks, selected via `frontend_framework`:

| Choice    | Value     | Stack                                                               |
| --------- | --------- | ------------------------------------------------------------------- |
| **Lit**   | `"lit"`   | Lit 4.x Web Components + Vite 6 + TypeScript 5.7+ + Tailwind CSS v4 |
| **React** | `"react"` | React 19 + Vite 6 + TypeScript 5.7+ + Tailwind CSS v4               |

Both share: Vite build, Vitest unit tests, ESLint 9 + typescript-eslint strict, Prettier 3.4, Zod 3.24 for runtime validation, pnpm 10 package manager, `.nvmrc` pinning Node version. Both produce `src/api/client.ts`, `src/models/schemas/`, `src/lib/utils.ts`, `src/styles/`.

#### Lit-specific files (when `frontend_framework == "lit"`)

- `src/app.ts` → Plain DOM mounting into `#app`
- `src/components/` → Lit `@customElement` decorators
- No JSX, no React-specific deps

#### React-specific files (when `frontend_framework == "react"`)

- `src/main.tsx` → `createRoot(document.getElementById('root')!).render(<App />)`
- `src/App.tsx` → Root React component
- `src/components/` → React functional components with typed props
- Additional deps: `react`, `react-dom`, `@types/react`, `@types/react-dom`
- JSX transform via `@vitejs/plugin-react`

### 4.2. `package.json.jinja` Specification

```json
{
  "name": "{{ project_slug }}-frontend",
  "private": true,
  "type": "module",
  "packageManager": "pnpm@10.x",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build --mode prod",
    "preview": "vite preview",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint .",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit"
  }
}
```

Dependencies: Conditional on `frontend_framework` — include `lit` OR `react`+`react-dom`. Always include: `vite`, `vitest`, `typescript`, `tailwindcss` (v4), `@tailwindcss/vite`, `zod`, `eslint`, `prettier`, `typescript-eslint`.

### 4.3. Frontend File Tree

```
frontend/
├── .nvmrc
├── Containerfile.jinja          # Multi-stage: builder (pnpm build), dev (vite dev), prod (serve)
├── eslint.config.js
├── index.html.jinja
├── package.json.jinja
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts               # @tailwindcss/vite plugin, /api proxy to :8000
├── vitest.config.ts             # happy-dom, 80% coverage thresholds
├── {% if use_playwright %}playwright.config.ts{% endif %}.jinja
├── public/
│   ├── favicon.svg
│   └── robots.txt
├── src/
│   ├── app.ts OR main.tsx       # Conditional on frontend_framework
│   ├── api/
│   │   └── client.ts            # Generic apiRequest<T>() fetch wrapper
│   ├── assets/.gitkeep
│   ├── components/
│   │   ├── common/.gitkeep
│   │   ├── layout/.gitkeep
│   │   └── ui/.gitkeep
│   ├── config/.gitkeep
│   ├── features/.gitkeep
│   ├── hooks/
│   │   └── index.ts
│   ├── lib/
│   │   └── utils.ts             # cn(), formatDate(), sleep()
│   ├── models/
│   │   ├── index.ts
│   │   ├── schemas/
│   │   │   └── index.ts         # Zod schemas mirroring backend Pydantic
│   │   └── types/
│   │       └── index.ts
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   └── index.ts
│   ├── styles/
│   │   ├── tailwind.css          # Tailwind v4 CSS-first @theme config
│   │   └── main.css
│   ├── templates/                # Jinja2 server-side templates
│   │   ├── base.html.j2
│   │   ├── layouts/default.html.j2
│   │   ├── pages/home.html.j2, dashboard.html.j2
│   │   ├── partials/header.html.j2, footer.html.j2
│   │   └── components/alert.html.j2
│   └── types/
│       └── index.ts
└── tests/
    ├── setup.ts                  # DOM cleanup, browser stubs, fetch helpers
    ├── unit/
    │   ├── api/client.test.ts
    │   ├── lib/utils.test.ts
    │   └── models/schemas.test.ts
    └── e2e/
        └── example.spec.ts       # Playwright (conditional)
```

### 4.4. TypeScript Strict Mode

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

---

## 5. AZURE INFRASTRUCTURE (`infra/`) — COMPLETE SPECIFICATION

The `infra/` directory is **conditionally included** when `cloud_provider == "azure"`. Follow the **two-tier Bicep deployment pattern** from the `claim_handler` reference project.

### 5.1. Bicep Module Architecture

```
{% if cloud_provider == 'azure' %}infra{% endif %}/
├── deploy.bicep.jinja              # Subscription-scoped entry: creates RG, delegates to main.bicep
├── main.bicep.jinja                # RG-scoped orchestrator: conditionally deploys all modules
├── README.md.jinja                 # Infrastructure documentation
├── modules/
│   ├── appInsights.bicep           # Application Insights (AAD-only auth, linked to Log Analytics)
│   ├── keyVault.bicep              # Key Vault (RBAC authorization, soft-delete, purge protection)
│   ├── logAnalytics.bicep          # Log Analytics Workspace (PerGB2018, configurable retention)
│   ├── {% if database_backend == 'azure_postgresql' %}postgres.bicep{% endif %}   # ← NEW: Azure Database for PostgreSQL Flexible Server
│   └── {% if use_redis %}redis.bicep{% endif %}                                    # ← NEW: Azure Cache for Redis (optional)
├── parameters/
│   ├── dev/deploy.dev.bicepparam.jinja
│   ├── test/deploy.test.bicepparam.jinja     # ← ADD test environment
│   ├── staging/deploy.staging.bicepparam.jinja  # ← ADD staging environment
│   └── prod/deploy.prod.bicepparam.jinja
└── scripts/
    ├── deploy.azcli.jinja          # Multi-env deployment script
    └── backup-db.zsh.jinja         # PostgreSQL backup script (when database_backend != "none")
```

### 5.2. `deploy.bicep.jinja` — Subscription Scope

```bicep
targetScope = 'subscription'

@description('Azure region for all resources')
param location string = '{{ azure_location }}'

@description('Project identifier (lowercase, hyphens)')
param projectName string = '{{ project_slug | replace("_", "-") }}'

@allowed(['dev', 'test', 'staging', 'prod'])
param environment string = 'dev'

param tags object = {
  project: projectName
  environment: environment
  managedBy: 'bicep'
}

var rgName = 'rg-${projectName}-${environment}'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: rgName
  location: location
  tags: tags
}

module main 'main.bicep' = {
  scope: rg
  name: 'main-${uniqueString(rg.id)}'
  params: {
    location: location
    projectName: projectName
    environment: environment
    tags: tags
  }
}

output resourceGroupName string = rg.name
output resourceGroupId string = rg.id
```

### 5.3. `main.bicep.jinja` — Resource Group Scope

Must include these feature-flagged modules with `enabled` parameter pattern:

| Module         | Parameter                                                             | Resource                                        |
| -------------- | --------------------------------------------------------------------- | ----------------------------------------------- |
| `logAnalytics` | `enableMonitoring`                                                    | Log Analytics Workspace                         |
| `appInsights`  | `enableMonitoring`                                                    | Application Insights (depends on Log Analytics) |
| `keyVault`     | `enableKeyVault`                                                      | Key Vault (RBAC, soft-delete, purge protection) |
| `postgres`     | `enablePostgres` (only when `database_backend == 'azure_postgresql'`) | Azure Database for PostgreSQL Flexible Server   |
| `redis`        | `enableRedis` (only when `use_redis`)                                 | Azure Cache for Redis                           |

All modules follow the pattern: `var namePrefix = '${sanitizedProject}-${environment}'`, derive resource name as `'${namePrefix}-suffix'`, accept optional custom name override.

### 5.4. NEW `modules/postgres.bicep` — Azure Database for PostgreSQL Flexible Server

```bicep
@description('PostgreSQL server name')
param name string

param location string
param tags object

@allowed(['B_Standard_B1ms', 'GP_Standard_D2s_v3', 'MO_Standard_E4s_v3'])
param skuName string = 'B_Standard_B1ms'

@allowed(['Burstable', 'GeneralPurpose', 'MemoryOptimized'])
param skuTier string = 'Burstable'

@minValue(1)
@maxValue(16)
param storageSizeGB int = 32

param administratorLogin string = 'pgadmin'
@secure()
param administratorPassword string

param postgresVersion string = '16'
param highAvailabilityMode string = 'Disabled'
param backupRetentionDays int = 7

param enabled bool = true

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = if (enabled) {
  name: name
  location: location
  tags: tags
  sku: {
    name: skuName
    tier: skuTier
  }
  properties: {
    version: postgresVersion
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorPassword
    storage: {
      storageSizeGB: storageSizeGB
    }
    backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: highAvailabilityMode
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
  }
}

// Allow Azure services to connect
resource firewallAllowAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2024-08-01' = if (enabled) {
  parent: postgres
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

output id string = enabled ? postgres.id : ''
output name string = enabled ? postgres.name : ''
output fqdn string = enabled ? postgres.properties.fullyQualifiedDomainName : ''
output connectionString string = enabled ? 'postgresql://${administratorLogin}@${postgres.name}:${administratorPassword}@${postgres.properties.fullyQualifiedDomainName}:5432/postgres?sslmode=require' : ''
```

### 5.5. NEW `modules/redis.bicep` — Azure Cache for Redis

```bicep
@description('Redis cache name')
param name string

param location string
param tags object

@allowed(['Basic', 'Standard', 'Premium'])
param skuFamily string = 'Basic'

@allowed(['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'])
param skuCapacity string = 'C0'

param enabled bool = true

resource redis 'Microsoft.Cache/redis@2024-03-01' = if (enabled) {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      name: skuFamily
      family: 'C'
      capacity: int(replace(skuCapacity, 'C', ''))
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    redisConfiguration: {}
  }
}

output id string = enabled ? redis.id : ''
output name string = enabled ? redis.name : ''
output hostName string = enabled ? redis.properties.hostName : ''
output sslPort int = enabled ? redis.properties.sslPort : 0
output primaryKey string = enabled ? redis.listKeys().primaryKey : ''
```

### 5.6. Deployment Scripts

- `scripts/deploy.azcli.jinja`: Wraps `az deployment sub create` with env-aware parameter resolution. Accepts `$1` (environment name, defaults to `dev`).
- `scripts/backup-db.zsh.jinja`: `pg_dump` with custom format, gzip compression, timestamped filenames. Only included when `database_backend != "none"`.

### 5.7. Parameter Files

Provide 4 environment parameter files: `dev`, `test`, `staging`, `prod`. Each toggles resource enabling:

| Resource                         | dev | test | staging | prod |
| -------------------------------- | --- | ---- | ------- | ---- |
| Key Vault                        | off | off  | on      | on   |
| Log Analytics                    | off | off  | on      | on   |
| App Insights                     | off | off  | on      | on   |
| PostgreSQL (if azure_postgresql) | on  | on   | on      | on   |
| Redis (if use_redis)             | off | off  | on      | on   |

---

## 6. DOCKER / COMPOSE — COMPLETE SPECIFICATION

### 6.1. `Containerfile.jinja` (Backend)

Multi-stage build:

- **builder**: `python:{{ python_version }}-slim`, copies uv from `ghcr.io/astral-sh/uv:latest`, installs deps with `uv sync --frozen --no-dev`
- **app-base**: Copies `.venv` and `src/`, creates non-root `appuser` (UID 1000)
- **dev**: Inherits app-base, installs dev deps, runs `uvicorn --reload`
- **prod**: Inherits app-base, runs `uvicorn` (no reload), adds HEALTHCHECK label

### 6.2. `compose.yml.jinja`

Services:

- `app` (backend, port 8000)
- `frontend` (port 3000)
- `caddy` (ports 80/443, conditional on `use_caddy`, profile `gateway`)
- `redis` (port 6379, conditional on `use_redis`)
- `db` (PostgreSQL 17, port 5432, conditional on `database_backend == "postgresql"`)
- `worker` + `beat` (Celery, conditional on `use_celery`)

All services must have healthchecks. Named volumes for persistent data. Two networks: `backend`, `frontend`.

### 6.3. Compose Overlays

- `compose.override.yml.jinja` — Dev: bind mounts, hot-reload via uvicorn `--reload`
- `compose.prod.yml.jinja` — Production: `read_only: true`, `no-new-privileges`, resource limits, Caddy multi-stage with baked-in frontend
- `compose.test.yml.jinja` — Test: tmpfs PostgreSQL (no persistence), Redis `--save ""` (no persistence)

---

## 7. OPENCODE INTEGRATION — NEW

When `with_opencode == true`, include:

### 7.1. `scripts/install/install-opencode.zsh.jinja`

```zsh
#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install OpenCode AI coding agent
# Usage: ./scripts/install/install-opencode.zsh [--npm | --brew | --skip-config]
```

Full install script (~175 lines) that:

1. Detects OS (linux/macos/windows/wsl)
2. Installs via official script (`curl -fsSL https://opencode.ai/install | bash`), npm (`npm install -g opencode-ai@latest`), or brew (`brew install anomalyco/tap/opencode`)
3. Scaffolds `opencode.json` config file with Anthropic/claude-opus-4-6 defaults
4. Creates `.opencode/plugins/` directory with README
5. Verifies installation (`opencode --version`)

### 7.2. `opencode.json.jinja`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "anthropic": {
      "name": "Anthropic"
    }
  },
  "model": {
    "build": "anthropic/claude-opus-4-6",
    "plan": "anthropic/claude-opus-4-6"
  },
  "instructions": "Follow the coding conventions in AGENTS.md and docs/conventions/."
}
```

### 7.3. `.opencode/plugins/`

```
{% if with_opencode %}.opencode{% endif %}/
├── plugins/
│   ├── example-plugin.js          # Plugin stub
│   └── README.md                  # Links to https://opencode.ai/docs/plugins
```

### 7.4. Integration Points

- Add `with_opencode` to `copier.yml` as a boolean (default: `false`)
- Add `install-opencode.zsh` to `scripts/install/install-all.zsh` (conditional)
- Add `install:opencode` task to `Taskfile.yml` (conditional)
- Mention OpenCode in `AGENTS.md` (already done)
- Add `opencode.json` to root (conditional)
- Add `.opencode/` directory (conditional)

---

## 8. SCRIPTS — COMPLETE SPECIFICATION

### 8.1. Install Scripts (`scripts/install/`)

| Script                                                                    | Conditional  | Purpose                                                  |
| ------------------------------------------------------------------------- | ------------ | -------------------------------------------------------- |
| `install-all.zsh.jinja`                                                   | —            | Orchestrator: runs all installers, prints summary        |
| `install-all.ps1.jinja`                                                   | —            | Windows PowerShell full setup (WSL2, Git, VS Code, etc.) |
| `install-git.zsh`                                                         | —            | Git + recommended config                                 |
| `install-zsh.zsh`                                                         | —            | Zsh + Oh My Zsh + plugins                                |
| `install-python.zsh.jinja`                                                | —            | uv + Python via `uv python install`                      |
| `install-node.zsh.jinja`                                                  | —            | fnm + Node + pnpm via corepack                           |
| `install-container.zsh.jinja`                                             | —            | Docker or Podman (based on `container_runtime`)          |
| `install-task.zsh`                                                        | —            | go-task CLI                                              |
| `install-vscode.zsh`                                                      | —            | VS Code + ~16 extensions (Linux/macOS)                   |
| `install-vscode.ps1`                                                      | —            | VS Code + extensions (Windows)                           |
| `install-wsl2.ps1`                                                        | —            | WSL2 + Ubuntu (Windows)                                  |
| `install-hadolint.zsh`                                                    | —            | Containerfile linter                                     |
| `install-shellcheck.zsh`                                                  | —            | Shell script linter                                      |
| `install-linters.zsh`                                                     | —            | hadolint + shellcheck + yamllint                         |
| `{% if cloud_provider != 'none' %}install-cloud-cli.zsh{% endif %}.jinja` | cloud        | Azure CLI (`az`) installer                               |
| `{% if use_caddy %}install-caddy.zsh{% endif %}`                          | caddy        | Caddy server                                             |
| `{% if use_redis %}install-redis.zsh{% endif %}.jinja`                    | redis        | Redis CLI tools                                          |
| `{% if use_devcontainer %}setup-devcontainer.zsh{% endif %}`              | devcontainer | Dev container setup                                      |
| `{% if with_opencode %}install-opencode.zsh{% endif %}.jinja`             | opencode     | **NEW**: OpenCode AI agent                               |

### 8.2. Operational Scripts (`scripts/`)

| Script                                                 | Purpose                                                        |
| ------------------------------------------------------ | -------------------------------------------------------------- |
| `bootstrap.zsh.jinja`                                  | Full bootstrap: prereqs → env → deps → registry → verify       |
| `setup.zsh.jinja`                                      | Quick setup: `uv sync` + `pnpm install` + `pre-commit install` |
| `health-check.zsh.jinja`                               | Curl health checks on backend + frontend                       |
| `run_migrations.zsh.jinja`                             | `alembic upgrade head`                                         |
| `seed_database.zsh.jinja`                              | Runs DB seed CLI command                                       |
| `{% if use_celery %}setup_celery.zsh{% endif %}.jinja` | Celery worker setup                                            |
| `{% if use_redis %}setup_redis.zsh{% endif %}.jinja`   | Redis configuration                                            |

All scripts: `.zsh` extension, `#!/usr/bin/env zsh`, `setopt ERR_EXIT PIPE_FAIL`, ShellCheck compliant.

---

## 9. NAMING REGISTRY — SINGLE SOURCE OF TRUTH

### 9.1. Purpose

The registry (`registry/naming_registry.json`) is the canonical definition for all shared identifiers: service names, ports, route paths, enum values, and field mappings. The generator (`registry/generate_registry.py`) reads this JSON and produces:

- **Python constants** → `backend/src/{{ project_slug }}/core/registry_constants.py`
- **TypeScript constants** → `frontend/src/config/registry_constants.ts`
- **Env ports** → `.env.ports`

### 9.2. File Tree

```
registry/
├── naming_registry.json.jinja
├── naming_registry.schema.json
├── generate_registry.py.jinja      # ~500 lines, supports --validate, --diff, --check modes
├── README.md.jinja
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_generate_registry.py
    └── test_generate_registry_property.py  # Hypothesis property tests
```

### 9.3. Workflow

- Edit `naming_registry.json` → run `task registry:generate` → commit generated files
- CI gate: `task registry:check` fails if generated files are stale
- Never hand-edit generated files

---

## 10. TASK RUNNER (`Taskfile.yml.jinja`) — COMPLETE TASK LIST

Use go-task with includes: `tasks/backend.yml`, `tasks/frontend.yml`, `tasks/docker.yml`.

### Core tasks:

| Task                                                                                         | Description                                                                 |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `setup`                                                                                      | Full project setup                                                          |
| `dev`                                                                                        | Start backend + frontend (parallel)                                         |
| `dev:backend`                                                                                | Backend only                                                                |
| `dev:frontend`                                                                               | Frontend only                                                               |
| `dev:db`                                                                                     | Database service only                                                       |
| `build`                                                                                      | Build frontend + backend for production                                     |
| `test`                                                                                       | Run all tests (registry + backend + frontend)                               |
| `test:unit`, `test:integration`, `test:property`, `test:performance`                         | Specific test suites                                                        |
| `test:e2e` (if playwright)                                                                   | Playwright E2E                                                              |
| `lint`                                                                                       | All linters (python, frontend, containers, shell, yaml, markdown, spelling) |
| `format`                                                                                     | Format all code                                                             |
| `typecheck`                                                                                  | Run type checkers (ty + tsc)                                                |
| `clean`                                                                                      | Clean build artifacts                                                       |
| `registry:generate`, `registry:validate`, `registry:check`, `registry:diff`, `registry:test` | Registry management                                                         |
| `db:migrate`, `db:revision`, `db:downgrade`, `db:seed`, `db:reset`                           | Database management                                                         |
| `pre-commit`                                                                                 | Run pre-commit on all files                                                 |
| `generate:types`                                                                             | Generate TypeScript types from OpenAPI schema                               |
| `security:audit`                                                                             | pip-audit + pnpm audit + detect-secrets                                     |
| `health`                                                                                     | Health check all services                                                   |
| `install`                                                                                    | Install all dependencies                                                    |
| `install:opencode` (if with_opencode)                                                        | Install OpenCode                                                            |

---

## 11. DOCUMENTATION — COMPLETE SPECIFICATION

### 11.1. Root Files

| File                    | Content                                                                                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md.jinja`       | Project landing page: prerequisites table, quickstart, task reference, API endpoints, architecture overview, license                                                             |
| `LICENSE.jinja`         | Conditional: MIT / Apache-2.0 / GPL-3.0 / Proprietary based on `license` variable. Uses `copyright_year` and `author_name`. Must produce a proper LICENSE _file_ (no extension). |
| `CONTRIBUTING.md.jinja` | Contributor guide: coding standards, branch naming, conventional commits, PR checklist                                                                                           |
| `SECURITY.md.jinja`     | Responsible disclosure policy                                                                                                                                                    |
| `CHANGELOG.md.jinja`    | Keep-a-Changelog format                                                                                                                                                          |
| `CODE_OF_CONDUCT.md`    | Contributor Covenant v2.1                                                                                                                                                        |
| `AGENTS.md.jinja`       | AI coding agent instructions (Copilot, Cursor, Cline, OpenCode)                                                                                                                  |

### 11.2. `docs/` Directory

| File                    | Content                                                   |
| ----------------------- | --------------------------------------------------------- |
| `API.md.jinja`          | REST API reference with request/response examples         |
| `ARCHITECTURE.md.jinja` | Hexagonal architecture deep dive with ASCII diagrams      |
| `CONFIG.md.jinja`       | Full environment variable reference                       |
| `CONTRIBUTING.md.jinja` | Developer contribution guide                              |
| `DEPLOYMENT.md.jinja`   | Deployment guide (Docker, Caddy, Azure, migrations)       |
| `DEVELOPMENT.md.jinja`  | Daily development reference                               |
| `DIAGRAMS.md.jinja`     | Mermaid diagrams (architecture, infrastructure, sequence) |
| `ONBOARDING.md.jinja`   | New developer onboarding                                  |
| `quickstart.md.jinja`   | Minimal quickstart                                        |
| `RELEASE.md.jinja`      | Release process (SemVer, conventional commits)            |
| `SETUP.md.jinja`        | Full setup guide                                          |
| `TESTING.md.jinja`      | Testing guide (pytest, vitest, Playwright, Hypothesis)    |
| `VSCODE.md.jinja`       | VS Code setup and extensions                              |

### 11.3. `docs/adr/` — Architecture Decision Records

| ADR                                    | Decision                                            |
| -------------------------------------- | --------------------------------------------------- |
| `0000-template.md.jinja`               | ADR template                                        |
| `0001-hexagonal-architecture.md.jinja` | Adopt hexagonal architecture                        |
| `0002-database-strategy.md.jinja`      | PostgreSQL or none; Azure Flexible Server for cloud |
| `0003-caddy-reverse-proxy.md.jinja`    | Caddy for reverse proxy                             |
| `0004-pydantic-settings.md.jinja`      | pydantic-settings for config                        |
| `0005-ruff-linting.md.jinja`           | Ruff for linting                                    |
| `0006-go-task.md.jinja`                | go-task over Make                                   |

### 11.4. `docs/conventions/` — Coding Standards

| File                    | Content                                         |
| ----------------------- | ----------------------------------------------- |
| `coding-style.md`       | Python + TypeScript + Shell style rules         |
| `error-handling.md`     | Exception hierarchy, error response format      |
| `git-workflow.md`       | Trunk-based dev, conventional commits, PR rules |
| `logging.md`            | structlog configuration, log levels             |
| `naming-conventions.md` | File, code, database, API naming patterns       |

### 11.5. `docs/diagrams/` — Mermaid Sources

```
architecture.mmd, data-flow.mmd, deployment.mmd, er-diagram.mmd
```

---

## 12. DEVCONTAINER & WORKSPACE

### 12.1. `.devcontainer/` (conditional on `use_devcontainer`)

- `Containerfile.dev.jinja` — Based on `mcr.microsoft.com/devcontainers/python:{{ python_version }}`, installs uv, pnpm, go-task, hadolint
- `compose.yml.jinja` — App + conditional Redis/PostgreSQL sidecars
- `devcontainer.json.jinja` — 20+ VS Code extensions, Python/TS settings, port forwarding, `postCreateCommand: "zsh scripts/setup.zsh"`

### 12.2. `{{ project_slug }}.code-workspace.jinja`

Multi-root VS Code workspace with folders: Root, Backend (src), Backend (tests), Frontend. Complete settings for Python (ruff), TypeScript (prettier), file associations, formatOnSave, rulers.

---

## 13. CADDY REVERSE PROXY (conditional on `use_caddy`)

### 13.1. `caddy/Caddyfile`

- Admin API disabled (`admin off`)
- Configurable domain via `$CADDY_DOMAIN` env var
- Security headers: `X-Frame-Options: DENY`, `Strict-Transport-Security`, CSP, HSTS
- Routes: `/health` → 200, `/api/*` → reverse proxy to backend, `/*` → static SPA (prod) or reverse proxy to Vite (dev)
- gzip + zstd compression

### 13.2. `caddy/Containerfile.jinja`

Multi-stage: builds frontend with pnpm, copies `dist/` into Caddy Alpine image.

---

## 14. MISCELLANEOUS FILES

| File                                    | Purpose                                                                             |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| `{{ _copier_conf.answers_file }}.jinja` | Copier answers YAML (for template updates)                                          |
| `cspell.json.jinja`                     | CSpell dictionaries + custom word list                                              |
| `renovate.json5`                        | Renovate bot: automerge minor/patch, manual merge for majors                        |
| `tox.ini.jinja`                         | Tox environments: lint, typecheck, test, test-unit, test-integration, test-property |
| `logs/.gitkeep`                         | Log directory placeholder                                                           |

---

## 15. TESTING — COMPLETE SPECIFICATION

### 15.1. Backend Testing

| Layer       | Location                     | Runner              | Purpose                                             |
| ----------- | ---------------------------- | ------------------- | --------------------------------------------------- |
| Unit        | `backend/tests/unit/`        | pytest              | Pure logic, no I/O, mirrors `src/` structure        |
| Integration | `backend/tests/integration/` | pytest              | Real DB / external services via `httpx.AsyncClient` |
| Property    | `backend/tests/property/`    | pytest + Hypothesis | Invariant testing for value objects, registry       |
| Performance | `backend/tests/performance/` | pytest              | Benchmarks and regression                           |

Markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`, `@pytest.mark.property`, `@pytest.mark.performance`

Test helpers: `factories/` (factory-boy), `fixtures/` (database, cache), `mocks/`, `utils/` (assertion helpers, fixture factory, mock builder)

### 15.2. Frontend Testing

| Layer               | Location               | Runner     | Purpose                               |
| ------------------- | ---------------------- | ---------- | ------------------------------------- |
| Unit                | `frontend/tests/unit/` | Vitest     | Component + utility tests (happy-dom) |
| E2E (if playwright) | `frontend/tests/e2e/`  | Playwright | Browser-based end-to-end              |

### 15.3. Registry Testing

| Location          | Runner | Purpose                                            |
| ----------------- | ------ | -------------------------------------------------- |
| `registry/tests/` | pytest | Unit + Hypothesis property tests for the generator |

### 15.4. Coverage Requirements

- Backend: 80% line coverage, branch coverage enabled
- Frontend: 80% line, branch, function, statement coverage

---

## 16. SECRET BACKEND — SPECIFICATION

### When `secret_backend == "env"` (default)

- All secrets via environment variables with `{{ project_slug | upper }}_` prefix
- `.env` files per environment (`.env`, `.env.dev`, `.env.prod`, `.env.test`)
- `pydantic-settings` loads `.env` files automatically

### When `secret_backend == "azure_kv"` (requires `cloud_provider == "azure"`)

- `azure-identity` + `azure-keyvault-secrets` dependencies
- `config/settings/base.py` includes `AZURE_KEY_VAULT_URL` setting
- A settings loader that fetches secrets from Azure Key Vault at startup
- Falls back to env vars if Key Vault is unavailable (for local development)
- Key Vault provisioned via `modules/keyVault.bicep` (RBAC, soft-delete, purge protection)
- Deploy script stores secrets: `az keyvault secret set --vault-name ... --name ... --value ...`

---

## 17. QUALITY & SECURITY

### 17.1. Linting

| Tool           | Target                       | Config                                          |
| -------------- | ---------------------------- | ----------------------------------------------- |
| Ruff           | Python (30+ rule categories) | `pyproject.toml [tool.ruff]`                    |
| ty             | Python type checking         | `pyproject.toml [tool.ty]`                      |
| ESLint 9       | TypeScript (strict, no-any)  | `eslint.config.js`                              |
| Prettier       | JS/TS/JSON/YAML/Markdown     | `.prettierrc`                                   |
| hadolint       | Containerfiles               | CLI                                             |
| ShellCheck     | Shell scripts                | CLI (bash mode, suppress zsh-specific warnings) |
| yamllint       | YAML files                   | `.yamllint.yml`                                 |
| markdownlint   | Markdown                     | CLI                                             |
| typos          | Spelling                     | CLI                                             |
| detect-secrets | Secret scanning              | `.secrets.baseline`                             |

### 17.2. Security

- pip-audit for Python dependency vulnerabilities
- pnpm audit for Node dependency vulnerabilities
- detect-secrets for leaked secrets
- Ruff bandit rules (S category) for Python security
- Non-root container user (UID 1000)
- `read_only` + `no-new-privileges` in production compose
- Rate limiting via slowapi
- Security headers via Caddy (HSTS, CSP, X-Frame-Options)
- JWT authentication with configurable expiry (when `use_auth`)

### 17.3. CI/CD Readiness

- Renovate bot for dependency updates (automerge minor/patch)
- pre-commit hooks
- Conventional commits (commitizen)
- tox for multi-environment testing
- `registry:check` as CI gate for generated file staleness

---

## 18. SUMMARY OF CHANGES FROM CURRENT STATE

This is what must change from the existing codebase:

| Area                 | Current                                                                        | Target                                                            |
| -------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| Cloud providers      | `none`, `azure`, `aws`, `gcp`                                                  | `none`, `azure` only                                              |
| Secret backends      | `env`, `azure_kv`, `aws_sm`, `gcp_sm`                                          | `env`, `azure_kv` only                                            |
| Database backends    | `postgresql`, `sqlite`                                                         | `none`, `postgresql`, `azure_postgresql`                          |
| Frontend framework   | Not parameterized (vanilla TS)                                                 | `lit` / `react` choice via `frontend_framework`                   |
| OpenCode             | Mentioned in AGENTS.md only                                                    | Full install script + config + `.opencode/` dir (optional)        |
| Azure infra modules  | 3 modules (Log Analytics, App Insights, Key Vault) + empty postgres/redis dirs | 5 modules (+ PostgreSQL Flexible Server, + Azure Cache for Redis) |
| Azure parameter envs | dev, prod                                                                      | dev, test, staging, prod                                          |
| Storage adapter      | S3 (AWS)                                                                       | Azure Blob Storage (when azure) + local fallback                  |
| S3 references        | `s3_storage_adapter.py`                                                        | Remove entirely, replace with Azure Blob                          |
| AWS/GCP deps         | boto3, google-cloud-secret-manager                                             | Remove entirely                                                   |
| SQLite deps          | aiosqlite                                                                      | Remove entirely                                                   |
| Backend bugs         | 7 known issues (see §2.4)                                                      | All fixed                                                         |
| Jinja indentation    | Broken in conditional blocks                                                   | Fixed                                                             |
| Missing protocols    | No EmailPort, no StoragePort                                                   | Added to `core/interfaces/`                                       |
| LICENSE file         | Exists as `LICENSE.jinja`                                                      | Ensure proper rendering (no `.jinja` suffix in output)            |
| `azure_location`     | Existed but need to verify                                                     | Copier var with `when` guard, default `swedencentral`             |
| Bicep API versions   | Mixed                                                                          | Standardize to latest stable (2024-xx-xx)                         |
| Naming consistency   | Mostly good                                                                    | Enforce `{project}-{env}-{suffix}` pattern in all Bicep           |

---

## 19. BEST PRACTICES ENFORCEMENT

- **Python**: PEP 695 generics, `type` statements, `X | Y` unions, `match` expressions, `from __future__ import annotations`, frozen dataclasses for immutability
- **TypeScript**: `strict: true`, `noUncheckedIndexedAccess`, no `any`, proper generics
- **Docker**: Multi-stage builds, non-root users, healthchecks, `.dockerignore`, image labels
- **Azure Bicep**: RBAC over access policies, AAD-only auth, soft-delete + purge protection, `enabled` parameter pattern, proper output chaining
- **Security**: Zero-trust defaults, least privilege, secrets never in code, rate limiting, CORS restrictions, security headers
- **Testing**: Comprehensive pyramid (unit → integration → property → e2e), 80% coverage floor, factory-boy for test data, Hypothesis for property testing
- **Documentation**: Every feature documented, ADRs for major decisions, onboarding guide, API reference, Mermaid diagrams
- **DX**: VS Code workspace with 20+ extensions, devcontainer, install scripts for every tool, Taskfile for all commands

---

_This prompt is the exhaustive specification. Every section, file, pattern, dependency, configuration, and convention has been captured from the comprehensive codebase analysis. Use it to rewrite the entire template, fixing all known bugs and implementing all specified changes._
