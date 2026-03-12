


- **Line length**: 99 characters
- **Quote style**: double quotes
- **Indent style**: 4 spaces
- **Line endings**: LF
- **Formatter**: `ruff format`
- **Linter**: `ruff check`


- All public functions, methods, and class attributes must have type hints
- No `Any` type — use proper generics, `Unknown`, or specific types
- Use `X | Y` union syntax (Python 3.12+)
- Use `collections.abc` over `typing` for generic types
- `from __future__ import annotations` in all files


- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Type aliases**: `PascalCase` with `type` statement


Google-style on all public modules, classes, functions, and methods:

```python
def create_user(email: str, name: str) -> User:
    """Create a new user with the given email and name.

    Args:
        email: The user's email address.
        name: The user's display name.

    Returns:
        The newly created user entity.

    Raises:
        ValidationError: If the email format is invalid.
    """
```


- Absolute imports only (no relative imports except in `__init__.py`)
- Order: stdlib → third-party → local (enforced by ruff isort)
- All `__init__.py` must define `__all__`


- **Core**: ZERO external imports — only stdlib and typing
- **Application**: imports core only — no framework imports
- **Ports**: imports application and core — FastAPI/Typer allowed
- **Adapters**: imports all inner layers — SQLAlchemy, httpx, redis allowed

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
