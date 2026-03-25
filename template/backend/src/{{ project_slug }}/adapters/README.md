# Adapters

External integrations and outbound port implementations (**driven / secondary
adapters**).

In Clean Architecture terminology, adapters in this directory are **Gateways**: they
implement the output port interfaces defined in `core/interfaces/` to connect the
Application Core to external tools (database, cache, email, etc.).

**Rules:**

- No business logic — only translation between external systems and internal interfaces.
- Each adapter implements an interface (protocol) defined in `core/interfaces/`.
- Adapters may depend on third-party libraries (SQLAlchemy, Redis, httpx, etc.).
- Dependency direction: adapters → core (never the reverse).

| Package        | Purpose                                         |
| -------------- | ----------------------------------------------- |
| `cache/`       | In-memory and Redis cache implementations       |
| `email/`       | SMTP and console email senders                  |
| `external/`    | HTTP client wrappers for third-party APIs       |
| `messaging/`   | Event bus implementations (in-memory)           |
| `persistence/` | ORM models, repositories, unit-of-work, mappers |
| `security/`    | Password hashing (PBKDF2PasswordHasher) adapter |
| `storage/`     | File storage (local filesystem, Azure Blob)     |
