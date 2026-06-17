# Quality Gate Skill

## Purpose

Ensure changes are production-ready by enforcing repeatable validation gates.

## Required checks

- lint and formatting checks
- type checks
- unit/integration tests (and property/e2e where applicable)
- pre-commit hooks
- template render validation for template changes

## Exit criteria

- no failing checks
- docs/config updated for behavior or setup changes
- architecture boundaries preserved