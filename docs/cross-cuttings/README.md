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

## Tooling baselines (canonical)

- **GitHub Actions majors**: root template-authoring workflows intentionally
  track newer majors (for example `actions/checkout@v6`) while generated
  template workflows stay on broadly adopted majors (`@v4`) unless a generated
  project requirement mandates newer versions.
- **markdownlint baseline**: root and template share core rules
  (`MD013/MD024/MD046/MD048`) with 88-column line length. Template keeps
  additional relaxed markdown rules to support broader generated-project docs
  variability.
- **MCP baseline**: canonical core set is `context7` + `shadcn`. Optional MCP
  servers (`storybook`, `playwright`, `gitnexus`, `azure`, `github`,
  `microsoft-docs`) are profile/capability-driven deltas.

## i18n

- i18n is currently not a hard-enforced cross-cutting baseline at template root.

## Key references

- `Taskfile.yml:13`
- `Taskfile.yml:25`
- `.pre-commit-config.yaml:8`
- `scripts/check-fastapi-status-codes.py:61`
- `docs/cross-cuttings/agentic-ownership-map.md`
- `docs/cross-cuttings/gitnexus-runbook.md`
