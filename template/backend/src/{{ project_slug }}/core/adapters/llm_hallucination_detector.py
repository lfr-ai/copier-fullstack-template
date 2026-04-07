from __future__ import annotations

from typing import List
from {{ project_slug }}.core.interfaces.llm import LLMGateway


class HallucinationDetector:
    """
    Implements hallucination detection and response grounding for LLMs.
    """

    def __init__(self, llm_gateway: LLMGateway):
        self.llm_gateway = llm_gateway

    async def detect_hallucination(
        self,
        *,
        user_query: str,
        context: List[str],
        llm_response: str,
    ) -> bool:
        """
        Detects hallucination by verifying response grounding against context.

        Args:
            user_query: The user's input query.
            context: Relevant context retrieved for grounding validation.
            llm_response: Generated response to validate.

        Returns:
            bool: If true, hallucination detected and response requires re-generation.
        """
        verification_prompt = (
            f"Given the user query: '{user_query}' and the provided context, determine if the following response is factually grounded: \n"
            f"{llm_response}"
        )

        result = await self.llm_gateway.complete(prompt=verification_prompt)
        return "not grounded" in result.lower()
