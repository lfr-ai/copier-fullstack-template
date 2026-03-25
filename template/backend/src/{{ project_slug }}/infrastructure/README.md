# Infrastructure

Low-level technical concerns that support the application.

This layer corresponds to the **Frameworks & Drivers** circle — the outermost ring in
Clean Architecture. It contains glue code for cross-cutting technical concerns that
don't implement a specific port interface.

| Package      | Purpose                              |
| ------------ | ------------------------------------ |
| `profiling/` | CPU, memory, and SQL query profiling |

- Infrastructure modules may import from `config/` and `core/` only.
- No business logic — only technical plumbing.
- Password hashing: `adapters/security/hashing.py` (implements
  `core.interfaces.PasswordHasher` port).
- Database health checks: `UnitOfWork.check_connection()` (via the UoW protocol).
