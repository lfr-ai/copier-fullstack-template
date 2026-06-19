# Quality Gate Skill

## Purpose

Ensure changes are production-ready by enforcing repeatable validation gates.

## Required checks

- lint and formatting checks (ruff, biome)
- type checks (ty, tsc)
- unit/integration tests (and property/e2e where applicable)
- pre-commit hooks
- architecture boundary checks

## Exit criteria

- no failing checks
- docs/config updated for behavior or setup changes
- architecture boundaries preserved
