# Ports

Primary (driving) adapters that expose application use-cases to the outside world.

In Ports & Adapters / Hexagonal terminology these are **driving adapters**: they receive
external input and translate it into calls on the Application Core.

> **Naming note:** Despite the directory name `ports/`, the actual _port interfaces_
> (protocols) live in `core/interfaces/`. This directory holds the driving **adapter**
> implementations — API controllers, CLI commands, and web controllers.
> The composition root lives in `composition/container.py`.

## Clean Architecture Mapping

| Clean Architecture Concept | Location in This Project                                                                                          |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Input Port**             | Application services / command handlers (`application/`)                                                          |
| **Output Port**            | Protocol interfaces (`core/interfaces/`)                                                                          |
| **Controller**             | API route handlers (`ports/api/routes/`), CLI commands (`ports/cli/`), web controllers (`ports/web/controllers/`) |
| **Presenter / ViewModel**  | API response schemas (`ports/api/schemas/`), web view models (`ports/web/view_models/`)                           |
| **Gateway**                | Protocol interfaces (`core/interfaces/`) + adapter implementations (`adapters/`)                                  |
| **Composition Root / DI**  | `composition/container.py`                                                                                        |

## Packages

| Package            | Purpose                                                           |
| ------------------ | ----------------------------------------------------------------- |
| `api/`             | FastAPI HTTP/REST interface                                       |
| `api/middleware/`  | Request/response middleware (CORS, auth, logging, …)              |
| `api/routes/`      | Endpoint modules grouped by resource (**controllers**)            |
| `api/schemas/`     | Request/response Pydantic schemas (**presentation layer**)        |
| `graphql/`         | Strawberry GraphQL schema, resolvers, permissions _(conditional)_ |
| `cli/`             | Click CLI commands                                                |
| `cli/commands/`    | Custom CLI command modules (scaffold)                             |
| `web/`             | Server-rendered HTML interface                                    |
| `web/controllers/` | Web page controllers (template rendering)                         |
| `web/view_models/` | Pydantic view models for template context (**presenter**)         |
| `web/forms/`       | Form definitions for server-rendered pages (scaffold)             |

> **Note:** The composition root / DI container has been moved to `composition/container.py`
> to enforce the clean architecture boundary — presentation should not own the wiring.

> **Note:** API versioning is handled via URL prefix (`API_V1_PREFIX = "/api/v1"` in
> `config/constants.py`), not by directory namespacing.

## Conventions

- Route modules import application services — never ORM models directly.
- Application services return **DTOs**, not domain entities. The route handler (acting
  as controller + presenter) maps DTOs to API response schemas.
- Use `dependencies.py` for reusable `Depends(...)` callables.
- `router.py` aggregates all sub-routers into a single `api_router`.
- Web controllers should use `view_models/` to build typed template context.
