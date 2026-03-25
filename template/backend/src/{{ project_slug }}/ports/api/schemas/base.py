"""Base schema for all API request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with shared API configuration.

    Public-facing API schemas inherit from 'BaseSchema'
    for consistent behaviour (whitespace stripping, etc.).
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
