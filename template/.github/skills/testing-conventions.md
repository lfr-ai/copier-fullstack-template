# Skill: Testing Conventions

## Purpose

Ensure tests match project structure, markers, and quality thresholds.

## Use This Skill When

- Adding tests for new code paths
- Expanding regression coverage
- Validating CI test failures

## Rules

- Mirror source structure under `backend/tests/` and `frontend/tests/`
- Use markers correctly: `unit`, `integration`, `property`, `performance`, `slow`
- Prefer factory-based test data and explicit edge-case coverage
- Keep coverage >= 80% for `core` + `application`

## Verification Commands

- `task test`
- `task test:unit`
- `task test:integration`
- `task test:property`
- `task test:coverage`
