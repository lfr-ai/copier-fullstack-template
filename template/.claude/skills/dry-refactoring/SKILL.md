---
name: dry-refactoring
description: Guided workflow to eliminate copy-paste duplication detected by jscpd.
---

# dry-refactoring

Eliminate copy-paste duplication using extract function, module, constant, or base class strategies.

## Workflow

1. Run `npx jscpd@4.0.5 --reporters ai <path>` to detect clones
2. Read both duplicated code fragments
3. Design refactoring (extract function/constant/base class/module)
4. Apply refactoring to both locations
5. Re-run jscpd to confirm elimination
6. Repeat for remaining clones