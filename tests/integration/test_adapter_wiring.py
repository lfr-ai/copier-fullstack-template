"""Integration tests for Self-CRAG and DeepRAG adapter wiring.

Verifies that pipelines correctly accept and use adapters via dependency injection.
Uses mock LLM and retriever gateways to verify the wiring pattern.
"""

from __future__ import annotations

import inspect

import pytest
from unittest.mock import AsyncMock

pytestmark = pytest.mark.integration


class TestDeepRAGAdapterWiring:
    """Integration tests for DeepRAGPipeline dependency injection."""

    def test_deep_rag_constructor_accepts_llm_and_retriever(self) -> None:
        """DeepRAGPipeline should accept LLM and retriever gateways."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()

        pipeline = DeepRAGPipeline(llm=mock_llm, retriever=mock_retriever)
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever

    def test_deep_rag_from_config_factory(self) -> None:
        """DeepRAGPipeline.from_config should wire dependencies from dict."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()

        pipeline = DeepRAGPipeline.from_config({
            "llm": mock_llm,
            "retriever": mock_retriever,
        })
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever

    def test_deep_rag_constructor_signature(self) -> None:
        """Verify DeepRAGPipeline constructor accepts keyword-only params."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        sig = inspect.signature(DeepRAGPipeline.__init__)
        params = sig.parameters
        assert "llm" in params
        assert "retriever" in params
        # Both should be keyword-only
        assert params["llm"].kind == inspect.Parameter.KEYWORD_ONLY
        assert params["retriever"].kind == inspect.Parameter.KEYWORD_ONLY


class TestSelfCRAGAdapterWiring:
    """Integration tests for SelfCRAGPipeline dependency injection."""

    def test_self_crag_constructor_accepts_llm_and_retriever(self) -> None:
        """SelfCRAGPipeline should accept LLM and retriever gateways."""
        from src.ai.rag.self_crag_pipeline import SelfCRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()

        pipeline = SelfCRAGPipeline(llm=mock_llm, retriever=mock_retriever)
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever

    def test_self_crag_from_config_factory(self) -> None:
        """SelfCRAGPipeline.from_config should wire dependencies from dict."""
        from src.ai.rag.self_crag_pipeline import SelfCRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()

        pipeline = SelfCRAGPipeline.from_config({
            "llm": mock_llm,
            "retriever": mock_retriever,
        })
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever


class TestKGAdapterProtocol:
    """Verify knowledge graph adapter protocol contracts."""

    @pytest.mark.asyncio
    async def test_networkx_kg_protocol_contract(self) -> None:
        """NetworkXKnowledgeGraph should satisfy KnowledgeGraphGateway protocol."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()

        # Test add_triplet
        await kg.add_triplet(
            subject="test_node", predicate="connects", obj="other_node"
        )

        # Test add_triplets
        await kg.add_triplets(
            [
                ("A", "relates_to", "B"),
                ("B", "relates_to", "C"),
            ]
        )

        # Test query_neighbors
        neighbors = await kg.query_neighbors(entity="test_node", depth=1)
        assert isinstance(neighbors, list)
