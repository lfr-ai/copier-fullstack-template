"""Prompt template management.

Store prompt templates as constants or load from files.
Keep prompts versioned and testable.
"""

from __future__ import annotations

from .registry import (
    PromptRegistryEditor,
    PromptVersionResolver,
    build_prompt_version_run_name,
    parse_version_overrides,
)


SYSTEM_DEFAULT = (
    "You are a helpful assistant. Respond concisely and accurately"
)

SUMMARIZE_TEMPLATE = (
    "Summarize the following text in {max_sentences} sentences or fewer:\n\n{text}"
)


def render_prompt(template: str, **kwargs: str | int) -> str:
    """Render a prompt template with the given variables.

    Args:
        template (str): Prompt template with {placeholders}.
        **kwargs (str | int): Variable substitutions.

    Returns:
        str: Rendered prompt string.
    """
    return template.format(**kwargs)


__all__ = [
    "PromptRegistryEditor",
    "PromptVersionResolver",
    "SYSTEM_DEFAULT",
    "SUMMARIZE_TEMPLATE",
    "build_prompt_version_run_name",
    "parse_version_overrides",
    "render_prompt",
]
