"""Standard error response schemas for API endpoints."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import BaseSchema

__all__ = ["ErrorDetail", "ErrorResponse"]


class ErrorDetail(BaseSchema):
    """Single error detail entry."""

    field: Annotated[str | None, Field(
        default=None,
        description="Field that caused the error",
        examples=["email", "password"],
    )]
    message: Annotated[str, Field(
        description="Human-readable error message",
        examples=["Field is required"],
    )]
    code: Annotated[str | None, Field(
        default=None,
        description="Machine-readable error code",
        examples=["REQUIRED", "INVALID_FORMAT"],
    )]


class ErrorResponse(BaseSchema):
    """Standard error response returned by API endpoints."""

    status: Annotated[int, Field(
        description="HTTP status code",
        examples=[400, 404, 500],
    )]
    message: Annotated[str, Field(
        description="Summary error message",
        examples=["Validation failed", "Resource not found"],
    )]
    errors: Annotated[list[ErrorDetail], Field(
        default_factory=list,
        description="Detailed errors",
        examples=[[{"field": "email", "message": "Field is required", "code": "REQUIRED"}]],
    )]
    request_id: Annotated[str | None, Field(
        default=None,
        description="Correlation request ID",
        examples=["req-abc123"],
    )]
