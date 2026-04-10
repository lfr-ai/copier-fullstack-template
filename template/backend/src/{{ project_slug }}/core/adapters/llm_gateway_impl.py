from {{ project_slug }}.core.adapters.llm_hallucination_detector import HallucinationDetector
from {{ project_slug }}.core.interfaces.reranker import RerankerGateway
from {{ project_slug }}.core.interfaces.llm import LLMGateway

class LLMGatewayImpl(LLMGateway):
    async def complete(self, *args, **kwargs):
        pass  # Replace with real implementation

    async def detect_hallucination(self, detector: HallucinationDetector, *args, **kwargs):
        result = await detector.detect_hallucination(llm_response=..., ...)
