"""User API response and request schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """User API response schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int = Field(..., gt=0, description="User identifier", examples=[1, 42])
    email: str = Field(..., description="User email address", examples=["user@example.com"])
    display_name: str = Field(..., description="User display name", examples=["Jane Doe"])
    is_active: bool = Field(True, description="Whether user is active", examples=[True])


class CreateUserRequest(BaseModel):
    """User creation request schema."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    email: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="User email address",
        examples=["user@example.com"],
    )
    display_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User display name",
        examples=["Jane Doe"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
        examples=["securepassword123"],
    )
