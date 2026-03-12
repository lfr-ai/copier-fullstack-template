---
description: Run a security audit on specified code or recent changes
agent: security-auditor
subtask: true
---

Perform a comprehensive security audit on:

$ARGUMENTS

Check for:

1. Input validation vulnerabilities
2. Injection attacks (SQL, command, template)
3. Authentication and authorization flaws
4. Data exposure risks (PII in logs, secrets in code)
5. Infrastructure security (CORS, headers, TLS)
6. Rate limiting and DoS protection
7. Dependency vulnerabilities

Output a risk-rated report with specific CWE references and remediation steps.
