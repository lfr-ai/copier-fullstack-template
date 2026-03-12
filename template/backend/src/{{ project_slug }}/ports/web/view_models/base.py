"""Base view model for template rendering."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["BaseViewModel"]


class BaseViewModel(BaseModel):
    """Base view model providing shared template context."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    title: Annotated[str, Field(
        default="",
        description="Page title for the HTML document",
        examples=["Dashboard", "User Profile"],
    )]
    messages: Annotated[list[str], Field(
        default_factory=list,
        description="Flash messages to display",
        examples=[["Settings saved"]],
    )]
    is_authenticated: Annotated[bool, Field(
        default=False,
        description="Whether the current user is authenticated",
        examples=[True, False],
    )]
