#!/usr/bin/env bash
# Guard against dangerous tool usage
# Additional tool-specific safety checks beyond guard-destructive

set -euo pipefail

# Read tool invocation from stdin or environment
if [ -n "${TOOL_INPUT:-}" ]; then
    TOOL_DATA="$TOOL_INPUT"
elif [ ! -t 0 ]; then
    TOOL_DATA=$(cat)
else
    # No input, nothing to check
    exit 0
fi

# Parse tool name and parameters
TOOL_NAME=$(echo "$TOOL_DATA" | jq -r '.tool // empty' 2>/dev/null || echo "")
TOOL_PARAMS=$(echo "$TOOL_DATA" | jq -r '.tool_input // empty' 2>/dev/null || echo "")

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Guard against writing to sensitive files
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
    FILE_PATH=$(echo "$TOOL_PARAMS" | jq -r '.file_path // .path // empty' 2>/dev/null || echo "")

    # Block writes to system config
    if [[ "$FILE_PATH" =~ ^/etc/ ]] || [[ "$FILE_PATH" =~ ^~/.ssh/ ]] || [[ "$FILE_PATH" =~ ^~/.aws/ ]]; then
        echo -e "${RED}❌ Blocked: Cannot write to system configuration${NC}" >&2
        echo -e "${RED}   File: $FILE_PATH${NC}" >&2
        exit 1
    fi

    # Warn about writing to .env files
    if [[ "$FILE_PATH" =~ \.env$ ]] || [[ "$FILE_PATH" =~ \.env\. ]]; then
        echo -e "${YELLOW}⚠️  Warning: Writing to environment file${NC}" >&2
        echo -e "${YELLOW}   File: $FILE_PATH${NC}" >&2
        echo -e "${YELLOW}   Ensure no secrets are hardcoded${NC}" >&2
    fi
fi

# Guard against Bash execution of package managers without uv/bun
if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$TOOL_PARAMS" | jq -r '.command // empty' 2>/dev/null || echo "$TOOL_PARAMS")

    # Block direct pip/npm without uv/bun
    if [[ "$COMMAND" =~ ^pip\ install ]] || [[ "$COMMAND" =~ ^npm\ install\ -g ]]; then
        echo -e "${RED}❌ Blocked: Use 'uv' for Python or 'bun' for Node.js${NC}" >&2
        echo -e "${RED}   Command: $COMMAND${NC}" >&2
        exit 1
    fi

    # Block execution of downloaded scripts
    if [[ "$COMMAND" =~ \|\ bash$ ]] || [[ "$COMMAND" =~ \|\ sh$ ]]; then
        echo -e "${RED}❌ Blocked: Cannot pipe to shell (curl | bash, wget | bash)${NC}" >&2
        echo -e "${RED}   Command: $COMMAND${NC}" >&2
        exit 1
    fi
fi

# All checks passed
exit 0
