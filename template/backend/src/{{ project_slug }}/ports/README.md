
Inbound adapters that expose application use-cases to the outside world.


| Package           | Purpose                                                     |
| ----------------- | ----------------------------------------------------------- |
| `api/`            | FastAPI HTTP/REST interface                                 |
| `api/middleware/` | Request/response middleware (CORS, auth, logging, …)        |
| `api/routes/`     | Endpoint modules grouped by resource                        |
| `api/schemas/`    | Request/response Pydantic schemas specific to API contracts |
| `api/v1/`         | Versioned namespace for API v1                              |
| `cli/`            | Typer/Click CLI commands                                    |
| `gateways/`       | Outbound port interfaces consumed by adapters               |
| `web/`            | Server-rendered HTML controllers (if applicable)            |


- Route modules import application services — never ORM models directly.
- Use `dependencies.py` for reusable `Depends(...)` callables.
- `router.py` aggregates all sub-routers into a single `api_router`.
