
Low-level technical concerns that support the application.


| Package       | Purpose                                                   |
| ------------- | --------------------------------------------------------- |
| `database/`   | Database health checks                                    |
| `scheduling/` | Background job scheduling (APScheduler / cron)            |
| `security/`   | Password hashing, encryption, JWT token handling, secrets |


- Infrastructure modules may import from `config/` and `core/` only.
- No business logic — only technical plumbing.
- All external service connections should be managed here.
- Connection pools must be properly configured per environment.
