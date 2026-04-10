---
description: Security conventions and OWASP compliance rules
applyTo: "**/*.py, **/*.ts, **/*.js, **/*.jinja"
---

# Security Instructions

## Forbidden Patterns

### Never Use

| Pattern | Risk | Alternative |
|---------|------|-------------|
| `eval()` / `exec()` | Code injection (CWE-94) | Explicit parsing, AST |
| `pickle.loads()` on untrusted data | Deserialization attack (CWE-502) | `json.loads()`, Pydantic |
| Raw SQL strings | SQL injection (CWE-89) | SQLAlchemy ORM |
| `subprocess(shell=True)` | Command injection (CWE-78) | `subprocess(shell=False)` with list args |
| `os.system()` | Command injection | `subprocess.run()` |
| Hardcoded secrets | Credential exposure (CWE-798) | Azure Key Vault, env vars |
| `yaml.load()` (unsafe) | Code execution | `yaml.safe_load()` |
| `tempfile.mktemp()` | Race condition | `tempfile.mkstemp()` |
| `assert` for validation | Stripped in -O mode | `if not ...: raise` |
| `.format()` / f-strings in SQL | SQL injection | Parameterized queries |

### API Security

- All routes MUST have rate limiting via `slowapi`
- All request bodies MUST be validated by Pydantic models
- CORS must be configured restrictively (specific origins, not `*`)
- Authentication tokens validated on every protected endpoint

### General

- Never log sensitive data (passwords, tokens, PII, secrets, API keys)
- Never commit `.env` files or private keys to source control
- Never expose stack traces in API error responses
- Use `secrets` module for token generation, not `random`
- Use `datetime.UTC` for timezone-aware security timestamps
- Validate all input at system boundaries (API routes, CLI, webhooks)
- Use HMAC for signature verification, not simple string comparison
- Container images run as non-root users
- Dependencies audited for known CVEs regularly
