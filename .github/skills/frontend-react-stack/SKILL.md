---
name: frontend-react-stack
description: Frontend React stack conventions for React 19, shadcn/ui, Storybook, Playwright, and clean UI architecture
applyTo: "template/frontend/**/*.{ts,tsx,css,json}"
---

# Frontend React Stack Skill

## Purpose

Use this skill for frontend template changes to keep the generated frontend
modern, testable, and AI-agent friendly.

## Core Conventions

- Keep a layered frontend structure: `application`, `domain`, `infrastructure`,
  `presentation`.
- Prefer shadcn/ui primitives and composition before custom low-level controls.
- Keep React components small and intention-revealing.
- Keep Storybook stories and docs synchronized with component behavior.

## Storybook Agentic Guidance

- Maintain Storybook with React + Vite and keep manifests useful for agents.
- Write focused stories (one concept per story) with descriptive purpose.
- Use JSDoc summaries/descriptions for components and props.
- Exclude instructional-only stories from manifests with `!manifest` tags.
- Add `play` functions for key interaction paths.

## Testing Guidance

- Use Vitest + RTL for component/unit behavior.
- Use Playwright for user journeys and accessibility checks.
- Prefer role-based selectors (`getByRole`) over brittle selectors.

## Documentation Expectations

- Update frontend docs when structure, tooling, or behavior changes.
- Keep examples aligned with current Storybook and Playwright setup.
