
Use cases, services, commands, queries, DTOs, and mappers.

**Rules:**

- Orchestration logic only — no framework imports.
- May import from `core/` — never the reverse.
- Services coordinate domain operations via repository/UoW interfaces.
- DTOs are immutable data containers for inter-layer communication.


| Package | Purpose |
|---|---|
| `commands/` | Write operations (CQRS command side) |
| `queries/` | Read operations (CQRS query side) |
| `dtos/` | Data Transfer Objects |
| `mappers/` | Entity ↔ DTO mappers |
| `services/` | Application services |
| `tasks/` | Background/async task definitions |
| `validators/` | Input validation logic |
