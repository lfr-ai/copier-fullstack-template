"""Shared fixtures for registry tests.

Ensures the registry package root is importable so test modules
can 'from generate_registry import …' without 'sys.path' hacks.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REGISTRY_DIR = Path(__file__).resolve().parent.parent
if str(_REGISTRY_DIR) not in sys.path:
    sys.path.insert(0, str(_REGISTRY_DIR))
