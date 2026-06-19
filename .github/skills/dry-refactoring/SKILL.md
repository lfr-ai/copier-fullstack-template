---
name: dry-refactoring
description: Guided workflow to eliminate copy-paste duplication detected by jscpd. Refactor clones using extract function, module, constant, or base class strategies.
---

# dry-refactoring

Guided workflow to eliminate copy-paste duplication in source code. Use after running [jscpd](../jscpd/SKILL.md) to detect clones.

## Prerequisites

First, run jscpd to identify duplications:

```bash
npx jscpd@4.0.5 --reporters ai <path>
```

See the **[jscpd](../jscpd/SKILL.md)** skill for full option reference.

## Workflow

1. Run jscpd with `--reporters ai` on the target path
2. Parse each clone line to identify the two duplicated locations (file + line range)
3. Read both code fragments from the source files
4. Understand what the duplicated code does
5. Design a refactoring: extract a shared function, class, module, or constant
6. Apply the refactoring — update both locations and all other usages
7. Re-run jscpd to confirm the clone is eliminated
8. Repeat for remaining clones, highest-impact first

## Refactoring Strategies

| Strategy | When |
|----------|------|
| Extract function | Same logic repeated with different inputs |
| Extract constant | Same literal values repeated |
| Extract base class | Parallel class hierarchies with shared behaviour |
| Extract module | Shared utilities across multiple modules |
| Template method | Same algorithm structure, different steps |
