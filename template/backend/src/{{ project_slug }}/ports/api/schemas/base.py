"""Base schema for all API request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

__all__ = ["BaseSchema"]


class BaseSchema(BaseModel):
    """Base schema with shared API configuration.

    All public-facing API schemas should inherit from this class
    to ensure consistent behaviour (whitespace stripping, etc.).
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
