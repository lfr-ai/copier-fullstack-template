"""Core type aliases and NewType definitions.

Keep domain-specific type aliases here so they can be shared across core
without importing from external packages.
"""

from __future__ import annotations

from typing import NewType

__all__ = ["UserId"]

UserId = NewType("UserId", str)
