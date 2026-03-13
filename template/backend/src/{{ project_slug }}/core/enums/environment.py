"""Deployment environment enumeration."""

from __future__ import annotations

from enum import auto, unique

from {{ project_slug }}.core.enums.base import ParseableEnum

__all__ = ["Environment"]


@unique
class Environment(ParseableEnum):
    """Deployment environment enumeration."""

    LOCAL = auto()
    DEV = auto()
    TEST = auto()
    STAGING = auto()
    PROD = auto()
