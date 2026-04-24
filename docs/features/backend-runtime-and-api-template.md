# Feature: backend runtime and api template

## Purpose and scope

Provides generated backend runtime scaffolding: environment-driven settings,
application factory wiring, middleware, and API route conventions.

## Analyzed files

- `template/backend/src/{{ project_slug }}/main.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/base.py.jinja`
- `template/backend/src/{{ project_slug }}/composition/container.py.jinja`
- `template/backend/src/{{ project_slug }}/config/settings/__init__.py.jinja`
- `template/backend/src/{{ project_slug }}/presentation/api/app.py.jinja`
- `template/backend/src/{{ project_slug }}/presentation/api/routes/*.py.jinja`
- `template/backend/pyproject.toml.jinja`
- `template/.env.example.jinja`

## Business rules and constraints

- Base settings use `BaseSettings` + `SettingsConfigDict`
  (`config/settings/base.py.jinja:21`, `:28`).
- Environment-class dispatch is centralized in `_SETTINGS_MAP` + `get_settings()`
  (`config/settings/__init__.py.jinja:18`, `:28`).
- API app factory controls route/middleware registration and lifecycle
  (`presentation/api/app.py.jinja:36`).
- Health probe endpoint is always available (`presentation/api/app.py.jinja:103`).
- HTTP status codes in routes use symbolic constants (`routes/*.py.jinja`, e.g.
  `routes/users.py.jinja:16`).

## Workflows (with code references)

1. Startup calls `setup_logging()` and creates `app` in `main.py.jinja`.
2. `create_api_app()` wires middleware and handlers (`app.py.jinja:66`, `:67`).
3. Route modules expose endpoint handlers with `status.HTTP_*` constants.
4. Settings are cached and reused per process (`config/settings/__init__.py.jinja:28`).

## Data models and dependencies

- `BaseAppSettings` is the central runtime config model.
- Typed fields define operational knobs: network, CORS, auth, AI, and integrations.
- AI runtime settings include optional LightRAG and RAG-Anything knobs for
  working directories, retrieval modes, parsers, and processing flags.
- RAG query payloads now support strategy-aware orchestration controls
  (`strategy`, `use_lightrag`, `lightrag_mode`, `combine_strategies`) so
  generated APIs can explicitly route across Self-CRAG, DeepRAG, and LightRAG.
- Generated dependencies include FastAPI, Pydantic, SQLAlchemy, and optional AI stacks
  (`template/backend/pyproject.toml.jinja:120`).

## Integrations

- FastAPI app and middleware stack.
- Optional Redis/Celery/Azure/LLM providers via feature flags.
- Optional LightRAG and RAG-Anything adapters are now wired in the composition
  container with typed settings and env-backed defaults.
- Adaptive RAG orchestration supports combined execution mode where Self-CRAG,
  DeepRAG, and LightRAG (when configured) run together with source/result
  aggregation and synthesis fallback behavior.
- DI container disposal on lifespan shutdown.

## API endpoints or UI components

- Core health endpoint in app factory (`presentation/api/app.py.jinja:103`).
- Route modules for users, workflows, documents, conversations, AI, and agents.

## Security and authorization

- Base settings validate insecure default secrets outside local env
  (`config/settings/base.py.jinja:425`).
- Error handling and rate limiting are always registered (`app.py.jinja:66`, `:67`).
- FastAPI status constants reduce ambiguity and keep transport semantics explicit.
