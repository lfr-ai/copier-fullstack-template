# Testing Conventions Skill

## Purpose

Provide consistent testing standards across backend, frontend, and template verification scripts.

## Conventions

- clear scenario-oriented naming
- isolate dependencies in unit tests
- cover edge cases and negative paths
- use factories/fixtures for repeated setup
- keep tests fast and deterministic

## Markers / levels

- unit: pure logic
- integration: adapter and boundary behavior
- property: invariants and parser/normalizer robustness
- e2e: user-critical workflows