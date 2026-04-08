"""End-to-end validation tests for DeepRAG pipeline.

Tests the DeepRAG and SelfCRAG pipelines at the construction
and factory level. Full async graph execution requires langgraph
and is tested in the template integration tests.
"""

from __future__ import annotations

import inspect

import pytest
from unittest.mock import AsyncMock


class TestDeepRAGPipelineE2E:
    """End-to-end construction tests for DeepRAGPipeline."""

    def test_deep_rag_from_config(self) -> None:
        """DeepRAGPipeline should be creatable from config dict."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()
        pipeline = DeepRAGPipeline.from_config({
            "llm": mock_llm,
            "retriever": mock_retriever,
        })
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever
        assert pipeline._graph is None  # Lazy

    def test_deep_rag_missing_llm_raises(self) -> None:
        """DeepRAGPipeline.from_config should reject missing llm."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        with pytest.raises(ValueError, match="llm is required"):
            DeepRAGPipeline.from_config({"retriever": AsyncMock()})

    def test_deep_rag_missing_retriever_raises(self) -> None:
        """DeepRAGPipeline.from_config should reject missing retriever."""
        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

        with pytest.raises(ValueError, match="retriever is required"):
            DeepRAGPipeline.from_config({"llm": AsyncMock()})


class TestSelfCRAGPipelineE2E:
    """End-to-end construction tests for SelfCRAGPipeline."""

    def test_self_crag_from_config(self) -> None:
        """SelfCRAGPipeline should be creatable from config dict."""
        from src.ai.rag.self_crag_pipeline import SelfCRAGPipeline

        mock_llm = AsyncMock()
        mock_retriever = AsyncMock()
        pipeline = SelfCRAGPipeline.from_config({
            "llm": mock_llm,
            "retriever": mock_retriever,
        })
        assert pipeline._llm is mock_llm
        assert pipeline._retriever is mock_retriever

    def test_self_crag_missing_llm_raises(self) -> None:
        """SelfCRAGPipeline.from_config should reject missing llm."""
        from src.ai.rag.self_crag_pipeline import SelfCRAGPipeline

        with pytest.raises(ValueError, match="llm is required"):
            SelfCRAGPipeline.from_config({"retriever": AsyncMock()})


class TestConfigLoaderPipelineCreation:
    """Test AIConfigLoader pipeline creation."""

    def test_config_loader_creates_deep_rag_pipeline(self) -> None:
        """AIConfigLoader should create DeepRAGPipeline from config."""
        from src.ai.config_loader import AIConfigLoader

        config = {
            "embeddings": {
                "test": {"type": "litellm", "model": "text-embedding-3-small", "dimension": 1536},
            },
            "llms": {
                "test": {"type": "litellm", "model": "gpt-4o", "api_key": "test-key"},
            },
            "vector_stores": {
                "test": {"type": "faiss", "dimension": 1536},
            },
            "retrievers": {
                "test": {
                    "type": "vector",
                    "embedding_ref": "embeddings.test",
                    "vector_store_ref": "vector_stores.test",
                },
            },
            "pipelines": {
                "deep_rag": {
                    "type": "deep_rag",
                    "llm_ref": "llms.test",
                    "retriever_ref": "retrievers.test",
                },
            },
        }

        loader = AIConfigLoader(config_dict=config)
        pipeline = loader.create_pipeline("deep_rag")

        from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline
        assert isinstance(pipeline, DeepRAGPipeline)


if __name__ == "__main__":
    unittest.main()
