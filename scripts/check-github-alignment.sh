#!/usr/bin/env bash
set -euo pipefail

# Verify template/.github core alignment conventions.
echo "Checking .github core alignment (agents/hooks/instructions/skills)..."

required_files="
template/.github/CODEOWNERS.jinja
template/.github/copilot-instructions.md.jinja
template/.github/agents/debug.agent.md
template/.github/agents/deep-thinking.agent.md
template/.github/agents/expert-react-frontend-engineer.agent.md
template/.github/agents/modernization.agent.md
template/.github/agents/prompt-engineering.agent.md
template/.github/agents/sdd.agent.md
template/.github/agents/tdd.agent.md
template/.github/hooks/hooks.json
template/.github/hooks/scripts/guard-tool.sh
template/.github/hooks/scripts/guard-tool.ps1
template/.github/hooks/scripts/check-licenses.sh
template/.github/hooks/scripts/check-licenses.ps1
template/.github/instructions/architecture.instructions.md.jinja
template/.github/instructions/coding-conventions.instructions.md
template/.github/instructions/commit.instructions.md
template/.github/instructions/frontend.instructions.md
template/.github/instructions/no-heredoc.instructions.md
template/.github/instructions/prompt.instructions.md
template/.github/instructions/shell.instructions.md
template/.github/instructions/testing.instructions.md.jinja
template/.github/instructions/update-docs-on-code-change.instructions.md
template/.github/skills/clean-architecture/SKILL.md
template/.github/skills/frontend-react-stack/SKILL.md
template/.github/skills/naming-registry/SKILL.md
template/.github/skills/python-conventions/SKILL.md
template/.github/skills/testing-conventions/SKILL.md
"

missing=0
for f in $required_files; do
  if [ ! -f "$f" ]; then
    echo "[FAIL] Missing required alignment file: $f"
    missing=1
  fi
done

# Legacy file guards — files that should NOT exist
legacy_files="
template/.github/agents/coordinator.agent.md
template/.github/agents/security-auditor.agent.md
template/.github/hooks/dependency-license-checker.json
template/.github/hooks/tool-guardian.json
template/.github/hooks/auto-format.json
template/.github/hooks/scripts/auto-format.sh
template/.github/hooks/scripts/auto-format.ps1
template/.github/hooks/scripts/scan-secrets.sh
template/.github/hooks/scripts/scan-secrets.ps1
template/.github/skills/shadcn-frontend/SKILL.md
template/.github/skills/README.md
"

for f in $legacy_files; do
  if [ -f "$f" ]; then
    echo "[FAIL] Legacy file found: $f (should be removed)"
    missing=1
  fi
done

[ "$missing" -eq 0 ] || exit 1
echo "[OK] .github core alignment checks passed"
