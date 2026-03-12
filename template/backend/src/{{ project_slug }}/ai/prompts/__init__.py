"""Prompt template management.

Store prompt templates as constants or load from files.
Keep prompts versioned and testable.
"""

from __future__ import annotations

__all__ = ["SUMMARIZE_TEMPLATE", "SYSTEM_DEFAULT", "render_prompt"]

from typing import Final

SYSTEM_DEFAULT: Final[str] = (
    "You are a helpful assistant. Respond concisely and accurately"
)

SUMMARIZE_TEMPLATE: Final[str] = (
    "Summarize the following text in {max_sentences} sentences or fewer:\n\n{text}"
)


def render_prompt(template: str, **kwargs: str | int) -> str:
    """Render a prompt template with the given variables.

    Args:
        template (str): Prompt template with {placeholders}.
        **kwargs: Variable substitutions.

    Returns:
        str: Rendered prompt string.
    """
    return template.format(**kwargs)
