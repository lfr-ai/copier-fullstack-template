---
name: "GitNexus: Impact Analysis"
description: Run impact workflow with GitNexus before code changes.
category: Analysis
tags: [gitnexus, architecture, risk]
---

Run a GitNexus impact workflow:

1. Start with semantic process discovery.
2. Inspect top candidate symbols.
3. Run upstream impact with depth 2-3.
4. Group findings as direct and transitive impact.
5. Recommend safest incremental implementation sequence.