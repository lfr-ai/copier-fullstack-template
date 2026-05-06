#!/usr/bin/env bash
# Check for license compatibility issues in dependencies
# This hook scans Python and Node.js dependencies for GPL/AGPL licenses
# that may conflict with the project's license (MIT).

set -euo pipefail

# Colors
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python dependencies
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    if command -v uv &> /dev/null; then
        echo "Checking Python dependencies for license issues..."

        # Check for GPL/AGPL licenses
        if uv pip list --format json 2>/dev/null | jq -r '.[] | select(.license | test("GPL|AGPL")) | "\(.name): \(.license)"' | grep -q .; then
            echo -e "${YELLOW}⚠️  Warning: Found GPL/AGPL licensed dependencies${NC}"
            uv pip list --format json 2>/dev/null | jq -r '.[] | select(.license | test("GPL|AGPL")) | "  - \(.name): \(.license)"'
            echo -e "${YELLOW}These may require license review.${NC}"
        fi
    fi
fi

# Check Node.js dependencies
if [ -f "package.json" ]; then
    if command -v npm &> /dev/null; then
        echo "Checking Node.js dependencies for license issues..."

        # Use license-checker if available
        if npx -y license-checker --summary 2>/dev/null | grep -iE "GPL|AGPL" &> /dev/null; then
            echo -e "${YELLOW}⚠️  Warning: Found GPL/AGPL licensed dependencies${NC}"
            npx -y license-checker --summary 2>/dev/null | grep -iE "GPL|AGPL" || true
            echo -e "${YELLOW}These may require license review.${NC}"
        fi
    fi
fi

# Non-blocking - always exit 0
exit 0
