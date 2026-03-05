"""Health check API routes."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return application health status.

    Returns:
        Health status payload.
    """
    return {"status": "healthy"}


@router.get("/health/ready")
async def readiness_check() -> dict[str, str]:
    """Return application readiness status.

    Returns:
        Readiness status payload.
    """
    return {"status": "ready"}
