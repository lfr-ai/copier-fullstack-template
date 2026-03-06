"""Generate project dependency graph using importlib."""

from __future__ import annotations

import ast
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def _parse_python_file(py_file: Path) -> ast.AST | None:
    """Parse Python file into AST.

    Args:
        py_file: Python file path.

    Returns:
        Parsed AST instance when parsing succeeds.
    """
    try:
        return ast.parse(py_file.read_text())
    except SyntaxError:
        return None


def _extract_imports(tree: ast.AST) -> list[str]:
    """Extract imported module names from AST.

    Args:
        tree: Parsed module AST.

    Returns:
        Imported module names.
    """
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


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
        tree = _parse_python_file(py_file)
        if tree is None:
            continue
        graph[relative] = _extract_imports(tree)

    return graph


def main() -> None:
    """Print dependency graph for project source."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    source_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    graph = analyze_imports(source_dir)

    for module, deps in sorted(graph.items()):
        if deps:
            logger.info("%s:", module)
            for dep in sorted(set(deps)):
                logger.info("  -> %s", dep)


if __name__ == "__main__":
    main()
