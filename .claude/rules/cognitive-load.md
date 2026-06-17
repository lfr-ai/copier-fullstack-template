---
paths:
  - "**/*.py"
---

# Cognitive Load

Write code for human brains. Working memory holds ~4 chunks simultaneously.

## Principles

1. **Deep modules over shallow** — simple interfaces hiding complex implementations.
2. **Locality of behavior** — keep related code together.
3. **Extract complex conditionals** — name intermediate booleans by business meaning.
4. **Early returns over nesting** — avoid deep nesting.
5. **Balanced DRY** — prefer minor duplication over poor abstractions.
6. **Comments for WHY** — code shows WHAT, comments explain constraints/intent.
7. **Composition over deep inheritance** — avoid hierarchy depth beyond 2 when possible.
8. **Self-descriptive values** — use enums/named constants over magic values.

## Validation

Before completion, verify:

- No function requires holding more than ~4 concepts in working memory.
- Complex conditionals are extracted into named intermediates.
- Nesting depth is minimized (prefer ≤2 levels).
- No shallow pass-through helpers without clarity value.
- Related behavior remains local and cohesive.
