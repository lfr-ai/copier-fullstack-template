"""Provide hallucination detection adapter for LLM responses."""

from __future__ import annotations

from ..interfaces.llm import LLMGateway


class HallucinationDetector:
    """Implement hallucination detection and response grounding for LLMs."""

    def __init__(self, llm_gateway: LLMGateway):
        self.llm_gateway = llm_gateway

    async def detect_hallucination(
        self,
        *,
        user_query: str,
        context: list[str],
        llm_response: str,
    ) -> bool:
        """Detect hallucination by verifying response grounding against context.

        Args:
            user_query (str): User input query.
            context (list[str]): Relevant context for grounding validation.
            llm_response (str): Generated response to validate.

        Returns:
            bool: True when hallucination is detected.
        """
        verification_prompt = (
            f"Given the user query: '{user_query}' and the provided context, determine if the following response is factually grounded: \n"
            f"{llm_response}"
        )

        result = await self.llm_gateway.complete(prompt=verification_prompt)
        return "not grounded" in result.lower()
