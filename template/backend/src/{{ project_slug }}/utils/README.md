# Utils

Pure-Python helper functions with **no framework or ORM dependencies**.

| Module                | Purpose                                            |
| --------------------- | -------------------------------------------------- |
| `crypto_utils.py`     | Hashing, token generation, encryption wrappers     |
| `file_utils.py`       | Filesystem operations and path sanitization        |
| `json_utils.py`       | JSON encoder with support for UUID, datetime, etc. |
| `logger_factory.py`   | Structlog logger factory / bound-logger helpers    |
| `pagination_utils.py` | In-memory list pagination helpers                  |
| `retry_policies.py`   | Tenacity retry decorator presets                   |
| `string_utils.py`     | Slug, truncation, and string manipulation          |
| `timing.py`           | Wall-clock timing context manager                  |

- No imports from `core/`, `application/`, `infrastructure/`, `presentation/`, or `config/`.
- Functions should be stateless and side-effect-free where possible.
- Keep modules focused: one concern per file.
