---
name: jscpd
description: Run jscpd clone detection and produce actionable duplication findings.
---

# jscpd

Identify copy/paste duplication before applying dry-refactoring.

## Usage

```bash
npx jscpd@4.0.5 --reporters ai --min-lines 10 --min-tokens 80 <path>
npx jscpd@4.0.5 -c jscpd.json .
```

This template uses a v4-oriented `jscpd.json` (`skipBlocks`), so keep the
CLI pinned to `4.0.5` unless config migration to v5+ is completed.
