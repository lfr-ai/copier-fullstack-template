# Composition Root

The **Composition Root** is the single place where concrete infrastructure classes are
wired to core interface protocols. In Clean Architecture this belongs at the
absolute outermost layer — it sees every concrete type but no other layer
references it except the application entry point (`main.py`).

| Module         | Purpose                                         |
| -------------- | ----------------------------------------------- |
| `container.py` | DI container — factory methods for all services |

## Rules

- Only `main.py` (or the ASGI entry point) and `presentation/api/dependencies.py`
  should import from this package.
- The container instantiates all concrete infrastructure implementations and injects
  them into application services via constructor keyword arguments.
- Third-party DI frameworks (e.g. `dependency-injector`, `lagom`) can be
  adopted here without affecting any other layer.
