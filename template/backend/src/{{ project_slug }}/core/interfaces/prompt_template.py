"""Prompt template gateway -- abstract interface for structured prompt management.

Concrete adapters may use LangChain's 'ChatPromptTemplate',
LlamaIndex's prompt system, or simple f-string templates.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class PromptTemplateGateway(Protocol):
    """Gateway for managing and rendering structured prompt templates."""

    def render(
        self,
        *,
        template_name: str,
        variables: dict[str, object],
    ) -> str:
        """Render a named prompt template with the given variables."""
        ...

    def list_templates(self) -> list[str]:
        """Return all registered template names."""
        ...

    def register_template(
        self,
        *,
        name: str,
        template: str,
        description: str = "",
    ) -> None:
        """Register a new prompt template."""
        ...
