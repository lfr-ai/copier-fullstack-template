"""Service health status enumeration."""

from __future__ import annotations

from enum import auto, unique

from {{ project_slug }}.core.enums.base import ParseableEnum

__all__ = ["ServiceStatus"]


@unique
class ServiceStatus(ParseableEnum):
    """Possible health statuses for a service or dependency."""

    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
