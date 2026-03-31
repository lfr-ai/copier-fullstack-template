# GitHub Copilot Agent Hooks

Hooks execute shell commands at key lifecycle points during Copilot agent sessions.
They provide deterministic automation for security, formatting, auditing, and compliance.

VS Code supports eight hook lifecycle events: `SessionStart`, `UserPromptSubmit`,
`PreToolUse`, `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`.

## Installed Hooks

| Hook            | File                              | Events                                         | Purpose                                         |
| --------------- | --------------------------------- | ---------------------------------------------- | ----------------------------------------------- |
| Tool Guardian   | `tool-guardian.json`              | `PreToolUse`                                   | Block dangerous operations                      |
| Session Logger  | `session-logger.json`             | All 8 events (PreToolUse/PostToolUse at DEBUG) | Audit trail                                     |
| Secrets Scanner | `secrets-scanner.json`            | `Stop`                                         | Scan for leaked credentials                     |
| Auto-Format     | `auto-format.json`                | `PostToolUse`                                  | Format files after edits                        |
| License Checker | `dependency-license-checker.json` | `Stop`                                         | Scan dependencies for copyleft licenses         |
| Context Saver   | `pre-compact.json`                | `PreCompact`                                   | Save working state and inject additionalContext |

## Scripts

All hook scripts live in `scripts/` with both shell (`.sh`) and PowerShell (`.ps1`)
variants for cross-platform support. Shell scripts target POSIX sh (not bash).

## Logs

Hook output is written to `logs/copilot/` (gitignored):

- `logs/copilot/tool-guardian/guard.log`
- `logs/copilot/sessions/session.log`
- `logs/copilot/secrets/scan.log`
- `logs/copilot/license-checker/check.log`
- `logs/copilot/context/compact.log`

## Configuration

Adjust behavior via environment variables in each hook's JSON file:

```json
{
    "hooks": {
        "PreToolUse": [
            {
                "type": "command",
                "command": ".github/hooks/scripts/guard-tool.sh",
                "windows": "powershell -ExecutionPolicy Bypass -File .github\\hooks\\scripts\\guard-tool.ps1",
                "env": {
                    "GUARD_MODE": "block"
                }
            }
        ]
    }
}
```

## Disabling

Set the skip variable in the hook's `env` block or remove the JSON file:

- `SKIP_TOOL_GUARD=true`
- `SKIP_LOGGING=true`
- `SKIP_SECRETS_SCAN=true`
- `SKIP_AUTO_FORMAT=true`
- `SKIP_LICENSE_CHECK=true`
- `SKIP_CONTEXT_SAVE=true`

## Safety

Hook scripts are protected from agent modification via `chat.tools.edits.autoApprove`
in `settings.json`. The agent must request manual approval before editing any file
under `.github/hooks/`.

## References

- [VS Code Hooks Documentation](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [awesome-copilot Hooks](https://awesome-copilot.github.com/hooks/)
