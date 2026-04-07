---
description: Security conventions applicable to all source code
applyTo: "**/*.py, **/*.ts, **/*.js, **/*.zsh"
---

- Never use 'eval()', 'exec()', '__import__()', or 'pickle.loads()' on untrusted input
- Never use raw SQL queries — always use SQLAlchemy ORM with parameterized queries
- Never log sensitive data (passwords, tokens, PII, secrets, API keys)
- Never hardcode secrets — use environment variables or secret backends
- Never commit '.env' files or private keys to source control
- Never use 'assert' for runtime input validation
- Never expose stack traces in API error responses
- Use 'secrets' module for token generation, not 'random'
- Use CORS with explicit allow-lists, not wildcard '*'
- Use rate limiting ('slowapi') on all API endpoints
- Use 'datetime.UTC' for timezone-aware security timestamps
- Validate all input at system boundaries (API routes, CLI, webhooks)
- Use HMAC for signature verification, not simple string comparison
- Container images run as non-root users
- Dependencies audited for known CVEs regularly
