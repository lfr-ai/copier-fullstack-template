"""Provide concrete LLM gateway adapter implementation."""

from __future__ import annotations

from .llm_hallucination_detector import HallucinationDetector
from ..interfaces.llm import LLMGateway
from ..interfaces.reranker import RerankerGateway

class LLMGatewayImpl(LLMGateway):
    async def complete(self, *args: object, **kwargs: object) -> str:
        """Generate completion using configured provider implementation."""
        raise NotImplementedError

    async def detect_hallucination(
        self,
        detector: HallucinationDetector,
        *,
        user_query: str,
        context: list[str],
        llm_response: str,
        reranker: RerankerGateway | None = None,
    ) -> bool:
        """Delegate hallucination detection to configured detector."""
        if reranker is not None:
            _ = reranker
        return await detector.detect_hallucination(
            user_query=user_query,
            context=context,
            llm_response=llm_response,
        )
