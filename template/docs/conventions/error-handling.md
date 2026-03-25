```text
DomainError
├── NotFoundError
├── ValidationError
├── AuthorizationError
└── ConflictError
```

All exceptions are defined in `core/exceptions/`.

1. **Always chain exceptions**: `raise NewError(...) from original_error`
2. **No bare `except`**: always catch specific exceptions
3. **No `assert` for runtime validation**: use explicit checks
4. **Core exceptions only**: never raise framework-specific exceptions from
   core/application
5. **Map at boundaries**: ports map core exceptions to HTTP errors (4xx/5xx)

```python
logger.error("user_not_found", user_id=user_id, error=str(err))

logger.error(f"User {user_id} not found: {err}")
```

---

All API errors return a consistent JSON structure:

```json
{
  "detail": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "params": { "user_id": "..." }
  }
}
```

HTTP status code mapping:

| Exception               | HTTP Status |
| ----------------------- | ----------- |
| `NotFoundError`         | 404         |
| `ValidationError`       | 422         |
| `AuthorizationError`    | 403         |
| `ConflictError`         | 409         |
| Unhandled `DomainError` | 500         |
