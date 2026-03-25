---
description: Verify MCP server availability, authentication and prompt-level readiness
agent: coordinator
---

# MCP Health Check

Validate MCP integration health for this project.

Required checks:

1. Confirm configured MCP servers exist in `opencode.json`.
2. Run MCP diagnostics for:
   - `context7`
   - `gh_grep`
3. Confirm Context7 readiness:
   - works without key for public docs lookups
   - if configured, `CONTEXT7_API_KEY` is detected and valid
4. Provide a pass/fail report with remediation steps.
5. Confirm provider/model readiness:
   - GitHub Copilot is connected (primary path)
   - If configured, additional providers are visible in model list
6. Confirm plugin readiness:
   - `oh-my-opencode` is enabled/loaded
   - `superpowers` is enabled/loaded (skills auto-registered)
7. Confirm companion-tool readiness (if used):
   - `gsd` available on PATH (installed via `npm install -g gsd-pi`)
   - GSD-2 commands usable (`/gsd`, `/gsd auto`, `/gsd status` inside session;
     `gsd headless status` for non-interactive checks)
   - GSD-2 doctor passes: `gsd headless doctor`

Then suggest two quick prompt checks:

- `Configure a Cloudflare Worker script to cache JSON API responses for five minutes. use context7`
- `What's the right way to set a custom domain in an SST Astro component? use the gh_grep tool`
