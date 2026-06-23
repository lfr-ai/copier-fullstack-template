# Frontend agentic best practices

This guide defines frontend-first agentic conventions for this template source
repository and its generated projects.

## Scope

- Root repo: template authoring workflows and validation.
- `template/`: generated-project workflows and runtime scaffolding.

## Storybook AI manifests

Use Storybook manifests as the primary component knowledge surface for agents.

- Keep stories focused: one concept per story.
- Add JSDoc summaries/descriptions to components and stories.
- Use `tags: ['!manifest']` for instructional-only stories/docs.
- Validate manifests in Storybook:
  - `/manifests/components.json`
  - `/manifests/docs.json`
  - `/manifests/components.html`

## Story quality rules

- Prefer CSF stories with explicit `args` and intentional naming.
- Avoid “kitchen sink” stories that mix unrelated concepts.
- Add `play` functions for critical interactions.
- Keep docs aligned with real behavior.

## Playwright strategy

Follow Playwright resilient testing practices:

- Prefer user-facing selectors:
  1. `getByRole`
  2. `getByLabel`
  3. `getByText`
  4. `getByTestId`
- Avoid CSS/XPath selectors unless no stable semantic selector exists.
- Keep tests isolated and deterministic.
- Use web-first assertions (`toBeVisible`, `toHaveText`, etc.).
- Use traces on failure in CI for debuggability.

## shadcn/ui conventions

- Prefer shadcn/ui primitives before custom low-level controls.
- Preserve composability and token-based styling.
- Keep component APIs predictable and strongly typed.

## Accessibility baseline

- Prefer semantic HTML and ARIA only when needed.
- Ensure keyboard navigation and visible focus states.
- Validate with Storybook accessibility checks and Playwright assertions.

## Frontend folder structure

Generated frontend projects should preserve layered boundaries:

- `domain/` for pure types/contracts.
- `application/` for use-case orchestration.
- `infrastructure/` for external integrations.
- `presentation/` for UI composition.

## References

- Storybook AI best practices: <https://storybook.js.org/docs/ai/best-practices>
- Storybook manifests: <https://storybook.js.org/docs/ai/manifests>
- Playwright best practices: <https://playwright.dev/docs/best-practices>
- shadcn/ui docs: <https://ui.shadcn.com/docs>
