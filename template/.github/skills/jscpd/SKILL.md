---
name: jscpd
description: Run jscpd clone detection and produce actionable duplication findings before dry refactoring.
---

# jscpd

Use this skill before `dry-refactoring` when you need to identify copy/paste
duplication in the codebase.

## Workflow

1. Run jscpd on the requested path.
2. Start with strict defaults to reduce noise.
3. If output is too noisy, increase minimum token/line thresholds.
4. Summarize findings as prioritized clone groups.
5. Hand off highest-impact clone groups to `dry-refactoring`.

## Recommended command patterns

```bash
npx jscpd@4.0.5 --reporters ai --min-lines 10 --min-tokens 80 <path>
```

For full-repo scan:

```bash
npx jscpd@4.0.5 -c jscpd.json .
```
