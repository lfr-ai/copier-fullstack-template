"""Base DTO definitions using Pydantic."""

from __future__ import annotations

from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


DataT = TypeVar("DataT")


class BaseDTO(BaseModel):
    """Base DTO with standard configuration."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        from_attributes=True,
    )


class PaginatedResponse(BaseDTO, Generic[DataT]):
    """Paginated response envelope for list endpoints."""

    items: list[DataT]
    total: Annotated[
        int,
        Field(ge=0, description="Total number of items available", examples=[42, 100]),
    ]
    offset: Annotated[
        int,
        Field(ge=0, description="Current offset in the result set", examples=[0, 20]),
    ]
    limit: Annotated[
        int,
        Field(gt=0, le=1000, description="Maximum items per page", examples=[20, 50]),
    ]

    @property
    def has_more(self) -> bool:
        """Check if more pages are available."""
        return (self.offset + self.limit) < self.total


class ErrorResponse(BaseDTO):
    """Standardized error response."""

    error_code: Annotated[
        str,
        Field(
            description="Machine-readable error code",
            examples=["VALIDATION_ERROR", "NOT_FOUND"],
        ),
    ]
    message: Annotated[
        str,
        Field(
            description="Human-readable error message",
            examples=["Resource not found"],
        ),
    ]
    details: Annotated[
        dict[str, object] | None,
        Field(default=None, description="Additional error context"),
    ]
