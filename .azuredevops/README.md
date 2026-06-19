# Azure DevOps governance

This folder contains pipeline and policy scaffolding for Azure DevOps projects.

## Files

| Path | Purpose |
| --- | --- |
| `pipelines/ci.yml` | CI quality gates for lint, type checks, tests, and security |
| `pipelines/renovate.yml` | Scheduled Renovate pipeline execution |
| `variables/ci.yml` | Shared CI variables |
| `variables/renovate.yml` | Shared Renovate variables |
| `templates/steps/setup-python.yml` | Reusable Python + uv setup |
| `templates/steps/setup-node.yml` | Reusable Node.js setup |
| `templates/steps/pre-commit.yml` | Reusable pre-commit hook execution |
| `policies/build-validation-main.json` | Example build-validation branch policy |
| `policies/required-reviewer-main.json` | Example required-reviewer branch policy |

## Notes

- Replace repository IDs, pipeline IDs, and reviewer IDs before policy apply.
- Enable OAuth token access for scheduled Renovate runs.
- Keep these assets project-agnostic.