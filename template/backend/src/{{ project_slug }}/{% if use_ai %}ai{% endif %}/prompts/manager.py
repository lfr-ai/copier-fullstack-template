"""Prompt template manager -- backward-compatibility alias.

Use 'Jinja2PromptTemplate' directly for new code.
"""

from typing import final

from .jinja2_templates import Jinja2PromptTemplate


@final
class PromptManager(Jinja2PromptTemplate):
    """Backward-compatible alias for :class:`Jinja2PromptTemplate`.

    Provides the legacy 'register(name, template)' and
    'render(name, **kwargs)' convenience API while delegating
    to the canonical Protocol-based implementation.
    """

    def register(self, name: str, template: str) -> None:  # type: ignore[override]
        """Register a template (legacy API)."""
        self.register_template(name=name, template=template)

    def render(self, name: str = "", **variables: object) -> str:  # type: ignore[override]
        """Render using the legacy positional name + kwargs API."""
        return super().render(template_name=name, variables=variables)
