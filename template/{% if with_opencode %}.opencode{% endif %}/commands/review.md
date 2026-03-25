---
description: Run a multi-perspective code review
subtask: true
---

Perform a thorough multi-perspective code review on the following:

$ARGUMENTS

Run these review perspectives in parallel using subagents:

1. **@reviewer** — Correctness, type safety, error handling, code quality
2. **@security-auditor** — Security vulnerabilities, injection risks, data exposure
3. **@architect** — Clean architecture compliance, Dependency Rule, dependency
   direction, reuse opportunities

After all reviews complete, synthesize findings into a prioritized summary with:

- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)
- Positive observations

Provide a clear verdict: APPROVE or REQUEST_CHANGES.
