"""LLM adapter implementations.

The primary adapter is :class:`~.litellm_adapter.LiteLLMAdapter` which
routes to 100+ providers via `LiteLLM <https://docs.litellm.ai/>`_.

The 'anthropic_adapter' module provides a convenience wrapper
that normalizes the 'anthropic/' model prefix.
"""
