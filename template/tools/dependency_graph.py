"""Generate project dependency graph using importlib."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def analyze_imports(source_dir: Path) -> dict[str, list[str]]:
    """Analyze Python imports in source directory.

    Args:
        source_dir: Path to source directory.

    Returns:
        Mapping of module paths to their imports.
    """
    graph: dict[str, list[str]] = {}

    for py_file in source_dir.rglob("*.py"):
        relative = str(py_file.relative_to(source_dir))
        try:
            tree = ast.parse(py_file.read_text())
        except SyntaxError:
            continue

        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)

        graph[relative] = imports

    return graph


def main() -> None:
    """Print dependency graph for project source."""
    source_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    graph = analyze_imports(source_dir)

    for module, deps in sorted(graph.items()):
        if deps:
            print(f"{module}:")
            for dep in sorted(set(deps)):
                print(f"  -> {dep}")


if __name__ == "__main__":
    main()
