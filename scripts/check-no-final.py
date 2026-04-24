"""Verify no Final[] type annotations on module-level constants.

Applies to public and internal constants/variables.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("template/backend/src")
pattern = re.compile(r"^[A-Z_][A-Z0-9_]*\s*:\s*Final", re.MULTILINE)
offenders: list[str] = []

for path in root.rglob("*"):
    if not path.is_file():
        continue
    if not (path.name.endswith(".py") or path.name.endswith(".py.jinja")):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if pattern.search(text):
        offenders.append(path.as_posix())

if offenders:
    print("[FAIL] Found Final[] annotations on module-level constants/variables:")
    for file in offenders:
        print(f"  - {file}")
    sys.exit(1)

print("[OK] No Final[] type annotations on module-level constants/variables")
