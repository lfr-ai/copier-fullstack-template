"""Unit tests for retriever factory methods (from_config).

Tests verify that all retrievers can be instantiated from configuration
dictionaries with proper validation of required parameters.
"""

from __future__ import annotations

import pytest


@pytest.mark.unit
class TestVectorRetrieverFactory:
    """Tests for VectorRetriever.from_config()."""

    def test_from_config_success(self) -> None:
        """VectorRetriever.from_config() creates instance with valid config."""
        from src.ai.rag.retrievers.vector_retriever import VectorRetriever

        # Create mock dependencies
        class MockEmbedding:
            async def embed_text(self, text: str) -> list[float]:
                return [0.1, 0.2, 0.3]

        class MockVectorStore:
            async def search(
                self,
                *,
                query_vector: list[float],
                top_k: int,
                filters: dict[str, object] | None = None,
            ) -> list[object]:
                return []

        config = {
            "embedding": MockEmbedding(),
            "vector_store": MockVectorStore(),
        }

        retriever = VectorRetriever.from_config(config)
        assert retriever is not None
        assert isinstance(retriever, VectorRetriever)

    def test_from_config_missing_embedding(self) -> None:
        """VectorRetriever.from_config() raises ValueError when embedding is missing."""
        from src.ai.rag.retrievers.vector_retriever import VectorRetriever

        class MockVectorStore:
            pass

        config = {
            "vector_store": MockVectorStore(),
        }

        with pytest.raises(ValueError, match="embedding is required"):
            VectorRetriever.from_config(config)

    def test_from_config_missing_vector_store(self) -> None:
        """VectorRetriever.from_config() raises ValueError when vector_store is missing."""
        from src.ai.rag.retrievers.vector_retriever import VectorRetriever

        class MockEmbedding:
            pass

        config = {
            "embedding": MockEmbedding(),
        }

        with pytest.raises(ValueError, match="vector_store is required"):
            VectorRetriever.from_config(config)

    def test_from_config_empty_config(self) -> None:
        """VectorRetriever.from_config() raises ValueError with empty config."""
        from src.ai.rag.retrievers.vector_retriever import VectorRetriever

        config: dict[str, object] = {}

        with pytest.raises(ValueError, match="embedding is required"):
            VectorRetriever.from_config(config)


@pytest.mark.unit
class TestEnsembleRetrieverFactory:
    """Tests for EnsembleRetriever.from_config()."""

    def test_from_config_success(self) -> None:
        """EnsembleRetriever.from_config() creates instance with valid config."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        # Create mock retriever
        class MockRetriever:
            async def retrieve(
                self,
                *,
                query: str,
                top_k: int,
                filters: dict[str, object] | None = None,
            ) -> list[object]:
                return []

        config = {
            "retrievers": [
                {"retriever": MockRetriever(), "weight": 0.6},
                {"retriever": MockRetriever(), "weight": 0.4},
            ]
        }

        retriever = EnsembleRetriever.from_config(config)
        assert retriever is not None
        assert isinstance(retriever, EnsembleRetriever)

    def test_from_config_single_retriever(self) -> None:
        """EnsembleRetriever.from_config() works with single retriever."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        class MockRetriever:
            async def retrieve(
                self,
                *,
                query: str,
                top_k: int,
                filters: dict[str, object] | None = None,
            ) -> list[object]:
                return []

        config = {
            "retrievers": [
                {"retriever": MockRetriever(), "weight": 1.0},
            ]
        }

        retriever = EnsembleRetriever.from_config(config)
        assert retriever is not None

    def test_from_config_default_weight(self) -> None:
        """EnsembleRetriever.from_config() uses default weight 1.0 when not specified."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        class MockRetriever:
            pass

        config = {
            "retrievers": [
                {"retriever": MockRetriever()},  # No weight specified
            ]
        }

        retriever = EnsembleRetriever.from_config(config)
        assert retriever is not None

    def test_from_config_missing_retrievers(self) -> None:
        """EnsembleRetriever.from_config() raises ValueError when retrievers is missing."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        config: dict[str, object] = {}

        with pytest.raises(ValueError, match="retrievers list is required"):
            EnsembleRetriever.from_config(config)

    def test_from_config_empty_retrievers_list(self) -> None:
        """EnsembleRetriever.from_config() raises ValueError with empty retrievers list."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        config = {
            "retrievers": []
        }

        with pytest.raises(ValueError, match="At least one retriever is required"):
            EnsembleRetriever.from_config(config)

    def test_from_config_retrievers_not_list(self) -> None:
        """EnsembleRetriever.from_config() raises ValueError when retrievers is not a list."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        config = {
            "retrievers": "not a list"
        }

        with pytest.raises(ValueError, match="retrievers must be a list"):
            EnsembleRetriever.from_config(config)

    def test_from_config_retriever_entry_not_dict(self) -> None:
        """EnsembleRetriever.from_config() raises ValueError when entry is not a dict."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        config = {
            "retrievers": ["not a dict"]
        }

        with pytest.raises(ValueError, match="each retriever entry must be a dict"):
            EnsembleRetriever.from_config(config)

    def test_from_config_missing_retriever_in_entry(self) -> None:
        """EnsembleRetriever.from_config() raises ValueError when retriever key is missing."""
        from src.ai.rag.retrievers.ensemble_retriever import EnsembleRetriever

        config = {
            "retrievers": [
                {"weight": 1.0}  # Missing retriever
            ]
        }

        with pytest.raises(ValueError, match="retriever is required in each entry"):
            EnsembleRetriever.from_config(config)


@pytest.mark.unit
class TestGraphRetrieverFactory:
    """Tests for GraphRetriever.from_config()."""

    def test_from_config_success(self) -> None:
        """GraphRetriever.from_config() creates instance with valid config."""
        from src.ai.rag.retrievers.graph_retriever import GraphRetriever

        # Create mock dependencies
        class MockKnowledgeGraph:
            async def query_neighbors(
                self,
                entity: str,
                *,
                depth: int,
                limit: int,
            ) -> list[dict[str, object]]:
                return []

        class MockLLM:
            async def complete(
                self,
                *,
                prompt: str,
                system_prompt: str | None = None,
                max_tokens: int = 128,
                temperature: float = 0.0,
            ) -> str:
                return "entity1, entity2"

        config = {
            "knowledge_graph": MockKnowledgeGraph(),
            "llm": MockLLM(),
            "depth": 3,
        }

        retriever = GraphRetriever.from_config(config)
        assert retriever is not None
        assert isinstance(retriever, GraphRetriever)

    def test_from_config_default_depth(self) -> None:
        """GraphRetriever.from_config() uses default depth when not specified."""
        from src.ai.rag.retrievers.graph_retriever import GraphRetriever

        class MockKnowledgeGraph:
            pass

        class MockLLM:
            pass

        config = {
            "knowledge_graph": MockKnowledgeGraph(),
            "llm": MockLLM(),
            # depth not specified
        }

        retriever = GraphRetriever.from_config(config)
        assert retriever is not None

    def test_from_config_missing_knowledge_graph(self) -> None:
        """GraphRetriever.from_config() raises ValueError when knowledge_graph is missing."""
        from src.ai.rag.retrievers.graph_retriever import GraphRetriever

        class MockLLM:
            pass

        config = {
            "llm": MockLLM(),
        }

        with pytest.raises(ValueError, match="knowledge_graph is required"):
            GraphRetriever.from_config(config)

    def test_from_config_missing_llm(self) -> None:
        """GraphRetriever.from_config() raises ValueError when llm is missing."""
        from src.ai.rag.retrievers.graph_retriever import GraphRetriever

        class MockKnowledgeGraph:
            pass

        config = {
            "knowledge_graph": MockKnowledgeGraph(),
        }

        with pytest.raises(ValueError, match="llm is required"):
            GraphRetriever.from_config(config)

    def test_from_config_empty_config(self) -> None:
        """GraphRetriever.from_config() raises ValueError with empty config."""
        from src.ai.rag.retrievers.graph_retriever import GraphRetriever

        config: dict[str, object] = {}

        with pytest.raises(ValueError, match="knowledge_graph is required"):
            GraphRetriever.from_config(config)
