"""Verify core layer has zero outward imports (Clean Architecture)."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("template/backend/src")
pattern = re.compile(
    r"\bfrom\s+[^\n]*\.(application|infrastructure|presentation|config|ai)\b"
)
offenders: list[str] = []

for path in root.rglob("*"):
    if not path.is_file():
        continue
    if "/core/" not in path.as_posix():
        continue
    if not (path.name.endswith(".py") or path.name.endswith(".py.jinja")):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if pattern.search(text):
        offenders.append(path.as_posix())

if offenders:
    print("[FAIL] Core layer contains outward imports:")
    for file in offenders:
        print(f"  - {file}")
    sys.exit(1)

print("[OK] Core layer has zero outward imports")
