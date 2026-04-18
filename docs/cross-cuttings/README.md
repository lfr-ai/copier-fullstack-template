# Cross-cutting analysis summary

## Error handling

- API app factory always registers centralized error handlers
  (`template/backend/src/{{ project_slug }}/presentation/api/app.py.jinja:66`).
- Settings validation guards insecure defaults and invalid runtime combinations
  (`template/backend/src/{{ project_slug }}/config/settings/base.py.jinja:425`).

## Security

- Secret scanning is enabled in pre-commit.
- Bandit and additional static checks run in repository quality gates.
- FastAPI status constant enforcement avoids ambiguous HTTP semantics.

## Data integrity

- Environment-specific settings classes reduce cross-environment leakage.
- Verification scripts protect architecture boundaries and coding invariants.

## Auditing and observability

- Logging is bootstrapped before app creation (`main.py.jinja`).
- Task + pre-commit workflow provides repeatable quality audit trails.

## i18n

- i18n is currently not a hard-enforced cross-cutting baseline at template root.

## Key references

- `Taskfile.yml:13`
- `Taskfile.yml:25`
- `.pre-commit-config.yaml:8`
- `scripts/check-fastapi-status-codes.py:61`
