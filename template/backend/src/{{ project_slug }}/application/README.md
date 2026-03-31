# Application

Use cases, services, commands, queries, DTOs, and mappers.

This layer corresponds to the **Application Business Rules** circle in Clean
Architecture. Services here define **Use Cases** — they specify what the outside world
can do with the system.

**Rules:**

- Orchestration logic only — no framework imports.
- May import from `core/` — never the reverse.
- Services coordinate domain operations via repository/UoW interfaces.
- Services accept DTOs and **return DTOs** — domain entities never leak beyond this
  layer. The `mappers/` module handles the conversion.
- DTOs are immutable data containers for inter-layer communication.

| Package     | Purpose                                                         |
| ----------- | --------------------------------------------------------------- |
| `commands/` | Write operations (CQRS command side)                            |
| `queries/`  | Read operations (CQRS query side)                               |
| `dtos/`     | Data Transfer Objects (input/output boundary)                   |
| `mappers/`  | Entity → DTO mappers (output boundary / presenter data shaping) |
| `services/` | Application services (use-case orchestrators)                   |
| `tasks/`    | Background/async task definitions                               |
