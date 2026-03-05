"""Deployment environment enumeration."""

from enum import StrEnum, auto, unique


@unique
class Environment(StrEnum):
    """Deployment environment enumeration."""

    LOCAL = auto()
    DEV = auto()
    TEST = auto()
    STAGING = auto()
    PRODUCTION = auto()
