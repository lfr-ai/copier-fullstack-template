
External integrations and outbound port implementations.

**Rules:**

- No business logic — only translation between external systems and internal interfaces.
- Each adapter implements an interface (protocol) defined in `core/interfaces/`.
- Adapters may depend on third-party libraries (SQLAlchemy, Redis, httpx, etc.).
- Dependency direction: adapters → core (never the reverse).


| Package | Purpose |
|---|---|
| `cache/` | In-memory and Redis cache implementations |
| `email/` | SMTP and console email senders |
| `external/` | HTTP client wrappers for third-party APIs |
| `messaging/` | Event bus implementations (memory, RabbitMQ) |
| `persistence/` | ORM models, repositories, unit-of-work, mappers |
| `storage/` | File storage (local filesystem, S3) |
