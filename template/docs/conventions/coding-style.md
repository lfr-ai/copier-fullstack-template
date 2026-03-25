- **Line length**: 88 characters (Ruff/Black standard)
- **Quote style**: double quotes
- **Indent style**: 4 spaces
- **Line endings**: LF
- **Formatter**: `ruff format`
- **Linter**: `ruff check`

- All public functions, methods, and class attributes must have type hints
- Avoid `Any` — prefer proper generics, `object`, or specific types. `Any` is permitted
  only at third-party library boundaries (e.g., LLM SDKs, LiteLLM kwargs) where the
  external API is inherently untyped
- Use `X | Y` union syntax (Python 3.12+)
- Use `collections.abc` over `typing` for generic types
- `from __future__ import annotations` in all files

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Type aliases**: `PascalCase` with `type` statement

Google-style on all public modules, classes, functions, and methods. Include type
annotations in docstring Args for quick reference:

```python
def create_user(email: str, name: str) -> User:
    """Create a new user with the given email and name.

    Args:
        email (str): The user's email address.
        name (str): The user's display name.

    Returns:
        User: The newly created user entity.

    Raises:
        ValidationError: If the email format is invalid.
    """
```

- Absolute imports only (no relative imports except in `__init__.py`)
- Order: stdlib → third-party → local (enforced by ruff isort)
- `__all__` in `__init__.py` where the package exposes a public API

### Layer Import Rules (Dependency Rule — Clean Architecture)

- **Core**: ZERO external imports — only stdlib and typing
- **Application**: imports core only — no framework imports. Application services access
  persistence via **UoW repository properties** (e.g. `uow.users`), NEVER by importing
  concrete adapter classes.
- **Ports**: imports application and core — FastAPI/Typer allowed
- **Adapters**: imports all inner layers — SQLAlchemy, httpx, redis allowed. Concrete
  repo instantiation belongs here (inside the UoW adapter).

---

- **Strict mode**: `strict: true` in `tsconfig.json`
- **No `any`**: use `unknown` or proper generics
- **Indent**: 2 spaces
- **Quotes**: single quotes (via Prettier)
- **Semicolons**: yes (via Prettier)
- **Formatter**: Prettier
- **Linter**: ESLint

---

- **Extension**: `.zsh`
- **Shebang**: `#!/usr/bin/env zsh`
- **Error handling**: `setopt ERR_EXIT PIPE_FAIL` at top
- **Variables**: always quoted `"${var}"`
- **Linter**: ShellCheck

---

[Conventional Commits](https://www.conventionalcommits.org/) format:

```text
type(scope): description

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`,
`build`, `revert`
