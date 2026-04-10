# Copilot Hooks

This directory contains [VS Code Copilot hooks](https://code.visualstudio.com/docs/copilot/copilot-extensibility-overview)
that run automatically during Copilot coding agent interactions.

## Active Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `tool-guardian.json` | PreToolUse | Blocks dangerous operations (force push, `rm -rf`, DB drops) |
| `auto-format.json` | PostToolUse | Auto-formats files after Copilot edits them |

## How Hooks Work

Hooks are JSON files that declare which Copilot event triggers them and what command
to run. The Copilot coding agent reads these automatically.

### PreToolUse Hooks

Run **before** a tool is executed. Can block the operation by returning a deny decision.
Used for safety guardrails.

### PostToolUse Hooks

Run **after** a tool completes. Used for cleanup, formatting, or validation.

## Environment Variables

### Tool Guardian

| Variable | Default | Description |
|----------|---------|-------------|
| `GUARD_MODE` | `block` | `block` denies dangerous ops, `warn` allows with warning |
| `SKIP_TOOL_GUARD` | (unset) | Set to `true` to disable |
| `TOOL_GUARD_LOG_DIR` | `logs/copilot/tool-guardian` | Log directory |
| `TOOL_GUARD_ALLOWLIST` | (empty) | Comma-separated patterns to skip |

### Auto-Format

| Variable | Default | Description |
|----------|---------|-------------|
| `SKIP_AUTO_FORMAT` | (unset) | Set to `true` to disable |

## Scripts

Hook scripts live in `scripts/` with cross-platform variants:

- `guard-tool.ps1` / `guard-tool.sh` — Tool Guardian implementation
- `auto-format.ps1` / `auto-format.sh` — Auto-format implementation

## Logs

Hook logs are written to `logs/copilot/` (git-ignored).
