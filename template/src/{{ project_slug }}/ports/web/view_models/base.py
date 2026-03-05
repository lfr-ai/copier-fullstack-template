"""Base view model for template rendering."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseViewModel(BaseModel):
    """Base view model providing shared template context."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = ""
    messages: list[str] = []
    is_authenticated: bool = False
