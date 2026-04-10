# Security Policy

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email the maintainers at **lfr@appension.dk**.

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Suggested fix, if any

## Response Timeline

| Action | Timeframe |
|--------|-----------|
| Acknowledgement | Within 48 hours |
| Initial assessment | Within 5 business days |
| Patch release | Within 30 days of confirmation |

## Scope

In scope for security reports:

- Template-generated code that introduces vulnerabilities in rendered projects
- `copier.yml` post-generation hooks that could execute unwanted commands
- Secrets or credentials accidentally committed to the repository
- CI/CD workflow configurations that expose secrets

Out of scope:

- Third-party dependencies (report upstream instead)
- Issues in projects generated from the template (those are the user's responsibility)
- Denial-of-service attacks against development environments

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest (`main`) | Yes |

## Security Measures

- Dependencies updated regularly via Renovate
- Pre-commit hooks to prevent credential leaks in generated projects
- GitHub Actions workflows use pinned action versions
- Template generates non-root container images with read-only filesystems
