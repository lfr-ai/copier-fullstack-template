---
name: gitnexus
description: Graph-powered code intelligence via GitNexus MCP server for impact analysis and dependency navigation.
---

# GitNexus Skill

Use GitNexus MCP tools for graph-powered code intelligence.

## When to Use

- Understanding code impact across the dependency graph
- Detecting which modules are affected by a change
- Navigating call graphs and dependency chains
- Analyzing architectural coupling

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `gitnexus_impact` | Analyze impact of a change on dependent code |
| `gitnexus_context` | Get rich context for a code symbol |
| `gitnexus_query` | Run custom graph queries |
| `gitnexus_detect_changes` | Detect what changed between commits |
| `gitnexus_route_map` | Map API routes to handler code |
| `gitnexus_shape_check` | Validate architectural shape rules |

## Workflow

1. Sync the graph after significant changes: `gitnexus_group_sync`
2. Before refactoring, check impact: `gitnexus_impact`
3. Use `gitnexus_context` to understand symbol relationships
4. After changes, validate with `gitnexus_shape_check`
