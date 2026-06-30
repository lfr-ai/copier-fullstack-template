# GitNexus runbook (template repo)

This runbook defines the minimum reliable workflow for graph-backed code
analysis in this repository.

## Scope

- Root repo index: `copier-fullstack-template`
- Template-source index (skip git root): `copier-template-source`

Both indexes are required for exhaustive analysis because many template files
live under `template/` and are not represented by the root index alone.

## Re-index workflow

Use full rebuild for deterministic analysis before large refactors:

```bash
gitnexus analyze --force --index-only --name copier-fullstack-template .
gitnexus analyze --force --index-only --skip-git --name copier-template-source template
```

## High-signal query workflow

1. List indexes and staleness.
2. Use Cypher for structural hotspots (functions/method counts by file).
3. Use `context` on candidate symbols to inspect incoming/outgoing edges.
4. Use `impact` before changing shared scripts or governance checks.

Example Cypher hotspots:

```cypher
MATCH (n:Function)
RETURN n.filePath AS file, count(*) AS functionCount
ORDER BY functionCount DESC
LIMIT 20
```

## Expected outputs

- `analyze`: node/edge/process counts and success banner.
- `context`: symbol content plus categorized refs/process participation.
- `impact`: risk level, depth-grouped blast radius, affected modules/processes.

## Pre-merge graph-backed consistency checklist

Use this checklist before merging script/governance/architecture changes:

1. Re-index both repository scopes (root + template source).
2. Run at least one structural Cypher query for touched areas.
3. Run `impact` on changed high-fanout symbols (`main`, shared check helpers,
   DI/container entrypoints).
4. Record risk and notable affected depth-1 callers in PR notes.

This process is intentionally manual in this environment (MCP query FTS can be
degraded), but it is now the required pre-merge graph-consistency gate.

## Known limitation

In this environment, MCP `query` may report FTS degradation even after
re-indexing. Treat Cypher + context/impact as authoritative fallback for
decision-making until FTS behavior stabilizes.
