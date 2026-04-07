"""Unit tests for adapter factory methods (from_config).

Tests that all adapters can be instantiated from configuration dictionaries
with sensible defaults and proper parameter validation.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.unit


class TestLiteLLMAdapterFactory:
    """Test factory method for LiteLLMAdapter."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (just model)."""
        from src.ai.llm.litellm_adapter import LiteLLMAdapter

        config = {"model": "gpt-4o"}
        adapter = LiteLLMAdapter.from_config(config)

        assert adapter.model == "gpt-4o"
        assert adapter is not None

    def test_from_config_all_parameters(self) -> None:
        """from_config() should accept all supported parameters."""
        from src.ai.llm.litellm_adapter import LiteLLMAdapter

        config = {
            "model": "gpt-4o-mini",
            "api_key": "sk-test-key",
            "api_base": "https://api.openai.com/v1",
            "api_version": "2024-02-01",
            "timeout": 45.0,
            "num_retries": 3,
            "drop_params": False,
        }
        adapter = LiteLLMAdapter.from_config(config)

        assert adapter.model == "gpt-4o-mini"

    def test_from_config_extra_kwargs(self) -> None:
        """from_config() should forward extra kwargs to constructor."""
        from src.ai.llm.litellm_adapter import LiteLLMAdapter

        config = {
            "model": "gpt-4o",
            "custom_param": "custom_value",
            "another_param": 42,
        }
        adapter = LiteLLMAdapter.from_config(config)

        assert adapter.model == "gpt-4o"

    def test_from_config_defaults(self) -> None:
        """from_config() should apply default values for missing parameters."""
        from src.ai.llm.litellm_adapter import LiteLLMAdapter
        from src.ai.config import DEFAULT_CHAT_MODEL

        config: dict[str, object] = {}
        adapter = LiteLLMAdapter.from_config(config)

        assert adapter.model == DEFAULT_CHAT_MODEL


class TestAnthropicAdapterFactory:
    """Test factory method for AnthropicAdapter."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (api_key only)."""
        from src.ai.llm.anthropic_adapter import AnthropicAdapter

        config = {"api_key": "sk-ant-test"}
        adapter = AnthropicAdapter.from_config(config)

        assert adapter is not None
        # Model should have anthropic/ prefix added
        assert "anthropic/" in adapter.model

    def test_from_config_all_parameters(self) -> None:
        """from_config() should accept all supported parameters."""
        from src.ai.llm.anthropic_adapter import AnthropicAdapter

        config = {
            "api_key": "sk-ant-test",
            "model": "claude-sonnet-4-20250514",
            "max_retries": 5,
            "timeout": 90.0,
            "default_headers": {"X-Custom": "header"},
        }
        adapter = AnthropicAdapter.from_config(config)

        assert "anthropic/" in adapter.model

    def test_from_config_missing_api_key(self) -> None:
        """from_config() should raise ValueError when api_key is missing."""
        from src.ai.llm.anthropic_adapter import AnthropicAdapter

        config: dict[str, object] = {}
        with pytest.raises(ValueError, match="api_key is required"):
            AnthropicAdapter.from_config(config)


class TestLangChainLLMAdapterFactory:
    """Test factory method for LangChainLLMAdapter."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (defaults)."""
        from src.ai.chains.langchain_adapter import LangChainLLMAdapter

        config: dict[str, object] = {}
        adapter = LangChainLLMAdapter.from_config(config)

        assert adapter is not None
        assert ":" in adapter.model  # Should have provider:model format

    def test_from_config_with_provider(self) -> None:
        """from_config() should accept provider parameter."""
        from src.ai.chains.langchain_adapter import LangChainLLMAdapter

        config = {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"}
        adapter = LangChainLLMAdapter.from_config(config)

        assert "anthropic:" in adapter.model

    def test_from_config_extra_kwargs(self) -> None:
        """from_config() should forward extra kwargs to LangChain."""
        from src.ai.chains.langchain_adapter import LangChainLLMAdapter

        config = {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
            "api_key": "sk-test",
        }
        adapter = LangChainLLMAdapter.from_config(config)

        assert adapter is not None


class TestLiteLLMEmbeddingAdapterFactory:
    """Test factory method for LiteLLMEmbeddingAdapter."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (defaults)."""
        from src.ai.embeddings.litellm_embeddings import LiteLLMEmbeddingAdapter

        config: dict[str, object] = {}
        adapter = LiteLLMEmbeddingAdapter.from_config(config)

        assert adapter is not None
        assert adapter.dimension > 0

    def test_from_config_all_parameters(self) -> None:
        """from_config() should accept all supported parameters."""
        from src.ai.embeddings.litellm_embeddings import LiteLLMEmbeddingAdapter

        config = {
            "model": "text-embedding-3-large",
            "dimension": 3072,
            "api_key": "sk-test",
            "api_base": "https://api.openai.com/v1",
            "api_version": "2024-02-01",
            "timeout": 30.0,
        }
        adapter = LiteLLMEmbeddingAdapter.from_config(config)

        assert adapter.model == "text-embedding-3-large"
        assert adapter.dimension == 3072


class TestSentenceTransformerEmbeddingAdapterFactory:
    """Test factory method for SentenceTransformerEmbeddingAdapter."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (defaults)."""
        from src.ai.embeddings.sentence_transformer_embeddings import (
            SentenceTransformerEmbeddingAdapter,
        )

        config: dict[str, object] = {}
        adapter = SentenceTransformerEmbeddingAdapter.from_config(config)

        assert adapter is not None
        assert adapter.dimension > 0

    def test_from_config_with_model_name(self) -> None:
        """from_config() should accept model_name parameter."""
        from src.ai.embeddings.sentence_transformer_embeddings import (
            SentenceTransformerEmbeddingAdapter,
        )

        config = {"model_name": "all-MiniLM-L6-v2"}
        adapter = SentenceTransformerEmbeddingAdapter.from_config(config)

        assert adapter.model == "all-MiniLM-L6-v2"


class TestFaissVectorStoreFactory:
    """Test factory method for FaissVectorStore."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (dimension only)."""
        from src.ai.vector_stores.faiss_store import FaissVectorStore

        config = {"dimension": 1536}
        store = FaissVectorStore.from_config(config)

        assert store is not None

    def test_from_config_with_persist_dir(self) -> None:
        """from_config() should accept persist_dir parameter."""
        from src.ai.vector_stores.faiss_store import FaissVectorStore

        config = {"dimension": 768, "persist_dir": "/tmp/faiss_test"}
        store = FaissVectorStore.from_config(config)

        assert store is not None

    def test_from_config_missing_dimension(self) -> None:
        """from_config() should raise KeyError when dimension is missing."""
        from src.ai.vector_stores.faiss_store import FaissVectorStore

        config: dict[str, object] = {}
        with pytest.raises(KeyError):
            FaissVectorStore.from_config(config)


class TestPgvectorStoreFactory:
    """Test factory method for PgvectorStore."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with database_url and dimension."""
        from src.ai.vector_stores.pgvector_store import PgvectorStore

        config = {
            "database_url": "postgresql://user:pass@localhost/db",
            "dimension": 1536,
        }
        store = PgvectorStore.from_config(config)

        assert store is not None

    def test_from_config_with_table_name(self) -> None:
        """from_config() should accept table_name parameter."""
        from src.ai.vector_stores.pgvector_store import PgvectorStore

        config = {
            "database_url": "postgresql://user:pass@localhost/db",
            "dimension": 768,
            "table_name": "custom_embeddings",
        }
        store = PgvectorStore.from_config(config)

        assert store is not None

    def test_from_config_missing_database_url(self) -> None:
        """from_config() should raise ValueError when database_url is missing."""
        from src.ai.vector_stores.pgvector_store import PgvectorStore

        config = {"dimension": 1536}
        with pytest.raises(ValueError, match="database_url is required"):
            PgvectorStore.from_config(config)

    def test_from_config_missing_dimension(self) -> None:
        """from_config() should raise KeyError when dimension is missing."""
        from src.ai.vector_stores.pgvector_store import PgvectorStore

        config = {"database_url": "postgresql://user:pass@localhost/db"}
        with pytest.raises(KeyError):
            PgvectorStore.from_config(config)


class TestAzureAISearchVectorStoreFactory:
    """Test factory method for AzureAISearchVectorStore."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with required parameters."""
        from src.ai.vector_stores.azure_ai_search_store import (
            AzureAISearchVectorStore,
        )

        config = {
            "endpoint": "https://my-search.search.windows.net",
            "api_key": "test-key",
            "index_name": "test-index",
        }
        store = AzureAISearchVectorStore.from_config(config)

        assert store is not None

    def test_from_config_with_dimension(self) -> None:
        """from_config() should accept dimension parameter."""
        from src.ai.vector_stores.azure_ai_search_store import (
            AzureAISearchVectorStore,
        )

        config = {
            "endpoint": "https://my-search.search.windows.net",
            "api_key": "test-key",
            "index_name": "test-index",
            "dimension": 3072,
        }
        store = AzureAISearchVectorStore.from_config(config)

        assert store is not None

    def test_from_config_missing_endpoint(self) -> None:
        """from_config() should raise ValueError when endpoint is missing."""
        from src.ai.vector_stores.azure_ai_search_store import (
            AzureAISearchVectorStore,
        )

        config = {"api_key": "test-key", "index_name": "test-index"}
        with pytest.raises(ValueError, match="endpoint is required"):
            AzureAISearchVectorStore.from_config(config)

    def test_from_config_missing_api_key(self) -> None:
        """from_config() should raise ValueError when api_key is missing."""
        from src.ai.vector_stores.azure_ai_search_store import (
            AzureAISearchVectorStore,
        )

        config = {
            "endpoint": "https://my-search.search.windows.net",
            "index_name": "test-index",
        }
        with pytest.raises(ValueError, match="api_key is required"):
            AzureAISearchVectorStore.from_config(config)

    def test_from_config_missing_index_name(self) -> None:
        """from_config() should raise ValueError when index_name is missing."""
        from src.ai.vector_stores.azure_ai_search_store import (
            AzureAISearchVectorStore,
        )

        config = {
            "endpoint": "https://my-search.search.windows.net",
            "api_key": "test-key",
        }
        with pytest.raises(ValueError, match="index_name is required"):
            AzureAISearchVectorStore.from_config(config)


class TestNeo4jKnowledgeGraphFactory:
    """Test factory method for Neo4jKnowledgeGraph."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (defaults)."""
        from src.ai.knowledge_graph.neo4j_adapter import Neo4jKnowledgeGraph

        config: dict[str, object] = {}
        graph = Neo4jKnowledgeGraph.from_config(config)

        assert graph is not None

    def test_from_config_all_parameters(self) -> None:
        """from_config() should accept all supported parameters."""
        from src.ai.knowledge_graph.neo4j_adapter import Neo4jKnowledgeGraph

        config = {
            "uri": "bolt://neo4j.example.com:7687",
            "username": "admin",
            "password": "secret123",
            "database": "knowledge_base",
        }
        graph = Neo4jKnowledgeGraph.from_config(config)

        assert graph is not None


class TestNetworkXKnowledgeGraphFactory:
    """Test factory method for NetworkXKnowledgeGraph."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (no persist_path)."""
        from src.ai.knowledge_graph.networkx_adapter import (
            NetworkXKnowledgeGraph,
        )

        config: dict[str, object] = {}
        graph = NetworkXKnowledgeGraph.from_config(config)

        assert graph is not None

    def test_from_config_with_persist_path(self) -> None:
        """from_config() should accept persist_path parameter."""
        from src.ai.knowledge_graph.networkx_adapter import (
            NetworkXKnowledgeGraph,
        )

        config = {"persist_path": "/tmp/graph.json"}
        graph = NetworkXKnowledgeGraph.from_config(config)

        assert graph is not None


class TestCrossEncoderRerankerFactory:
    """Test factory method for CrossEncoderReranker."""

    def test_from_config_minimal(self) -> None:
        """from_config() should work with minimal config (defaults)."""
        from src.ai.rag.rerankers.cross_encoder import CrossEncoderReranker

        config: dict[str, object] = {}
        reranker = CrossEncoderReranker.from_config(config)

        assert reranker is not None

    def test_from_config_with_model_name(self) -> None:
        """from_config() should accept model_name parameter."""
        from src.ai.rag.rerankers.cross_encoder import CrossEncoderReranker

        config = {"model_name": "cross-encoder/ms-marco-MiniLM-L-12-v2"}
        reranker = CrossEncoderReranker.from_config(config)

        assert reranker is not None
