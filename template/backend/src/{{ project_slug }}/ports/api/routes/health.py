"""Health check API routes."""

from __future__ import annotations

from typing import Final

from fastapi import APIRouter

from {{ project_slug }}.core.enums import ServiceStatus
from {{ project_slug }}.ports.api.schemas.health import DependencyHealth, HealthResponse

__all__ = ["health_check", "readiness_check", "router"]

router: Final[APIRouter] = APIRouter()

_APP_VERSION: Final[str] = "0.1.0"
"""Application version — keep in sync with pyproject.toml."""


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return application health status.

    Returns:
        HealthResponse: Aggregate health status payload.
    """
    return HealthResponse(
        status=ServiceStatus.HEALTHY,
        version=_APP_VERSION,
        dependencies=[],
    )


@router.get("/health/ready", response_model=HealthResponse)
async def readiness_check() -> HealthResponse:
    """Return application readiness status.

    Checks connectivity to critical dependencies
    (database, cache, etc.) and reports their health.

    Returns:
        HealthResponse: Readiness status with dependency health details.
    """
    deps: list[DependencyHealth] = []

    # TODO: inject actual dependency health checks via DI
    # Example pattern for database:
    # start = time.perf_counter()
    # try:
    #     await db_session.execute(text("SELECT 1"))
    #     latency = (time.perf_counter() - start) * 1000
    #     deps.append(DependencyHealth(name="database", status=ServiceStatus.HEALTHY, latency_ms=latency))
    # except Exception as exc:
    #     deps.append(DependencyHealth(name="database", status=ServiceStatus.UNHEALTHY, message=str(exc)))

    overall = (
        ServiceStatus.HEALTHY
        if all(d.status == ServiceStatus.HEALTHY for d in deps)
        else ServiceStatus.DEGRADED
    )
    return HealthResponse(
        status=overall,
        version=_APP_VERSION,
        dependencies=deps,
    )
