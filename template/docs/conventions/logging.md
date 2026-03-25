# Logging

We use [structlog](https://www.structlog.org/) for structured logging.

- **Development**: human-readable console output with colors
- **Production**: JSON format for log aggregation
- **Test**: minimal output, captured by pytest

1. **Never use `print()`** — always use logging
2. **Never use f-strings in log calls** — use `%s` formatting or structlog key-value
   pairs
3. **Always include context** — who, what, why

```python
import structlog

logger = structlog.get_logger(__name__)

logger.info("user_created", user_id=user.id, email=user.email)
logger.error("payment_failed", order_id=order.id, error=str(err))
logger.warning("rate_limit_exceeded", ip_address=request.client.host)

# Bad — f-string in log call:
# logger.info(f"User {user.id} created")
```

| Level      | Usage                                   |
| ---------- | --------------------------------------- |
| `DEBUG`    | Detailed diagnostic info (dev only)     |
| `INFO`     | Normal operation events                 |
| `WARNING`  | Unexpected but recoverable situations   |
| `ERROR`    | Failures that affect a single operation |
| `CRITICAL` | System-level failures                   |

Every HTTP request gets a unique request ID via the `request_id` middleware. This ID is
automatically included in all log entries and response headers (`X-Request-ID`).
