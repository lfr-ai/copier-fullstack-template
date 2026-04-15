"""Create a VCS-free copy of the template source for rendering."""
from pathlib import Path
import shutil
import sys

src = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
dst = Path(sys.argv[2])
exclude = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None

IGNORED = {
    ".git", ".venv", "node_modules", ".mypy_cache",
    ".ruff_cache", ".pytest_cache", "__pycache__",
}


def ignore(path: str, names: list[str]) -> set[str]:
    p = Path(path).resolve()
    if exclude and p == exclude:
        return set(names)
    return {name for name in names if name in IGNORED}


shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)
print(f"[OK] Template snapshot created at {dst}")
