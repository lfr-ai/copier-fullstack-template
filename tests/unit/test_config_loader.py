"""Unit tests for AIConfigLoader with reference resolution and caching."""

from __future__ import annotations

import os
import pytest
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

if TYPE_CHECKING:
    from ai.config_loader import AIConfigLoader


@pytest.fixture
def mock_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set a test environment variable."""
    monkeypatch.setenv("TEST_API_KEY", "sk-test-12345")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-test")


@pytest.fixture
def simple_config_dict() -> dict:
    """Minimal valid config dict."""
    return {
        "embeddings": {
            "default": {
                "type": "litellm",
                "model": "text-embedding-3-small",
                "dimension": 1536,
            }
        },
        "llms": {
            "gpt4": {
                "type": "litellm",
                "model": "gpt-4o",
            }
        },
        "vector_stores": {
            "faiss": {
                "type": "faiss",
                "dimension": 1536,
            }
        },
    }


@pytest.fixture
def full_config_dict() -> dict:
    """Full config with retrievers and pipelines."""
    return {
        "embeddings": {
            "default": {
                "type": "litellm",
                "model": "text-embedding-3-small",
                "dimension": 1536,
            }
        },
        "llms": {
            "gpt4": {
                "type": "litellm",
                "model": "gpt-4o",
            }
        },
        "vector_stores": {
            "faiss": {
                "type": "faiss",
                "dimension": 1536,
            }
        },
        "retrievers": {
            "vector": {
                "type": "vector",
                "embedding_ref": "embeddings.default",
                "vector_store_ref": "vector_stores.faiss",
            }
        },
        "pipelines": {
            "self_crag": {
                "type": "self_crag",
                "llm_ref": "llms.gpt4",
                "retriever_ref": "retrievers.vector",
            }
        },
    }


@pytest.fixture
def config_with_env_vars() -> dict:
    """Config with environment variable substitution."""
    return {
        "llms": {
            "gpt4": {
                "type": "litellm",
                "model": "gpt-4o",
                "api_key": "${TEST_API_KEY}",
            }
        }
    }


@pytest.fixture
def config_yaml_file(tmp_path: Path, full_config_dict: dict) -> Path:
    """Create a temporary YAML config file."""
    import yaml

    config_path = tmp_path / "test_config.yaml"
    with config_path.open("w") as f:
        yaml.dump(full_config_dict, f)
    return config_path


class TestAIConfigLoaderInit:
    """Test AIConfigLoader initialization."""

    def test_init_with_config_dict(self, simple_config_dict: dict) -> None:
        """Test initialization with config_dict."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        assert loader is not None
        assert "embeddings" in loader._config
        assert "llms" in loader._config

    def test_init_with_config_path(self, config_yaml_file: Path) -> None:
        """Test initialization with config_path."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_path=config_yaml_file)
        assert loader is not None
        assert "embeddings" in loader._config
        assert "pipelines" in loader._config

    def test_init_without_config_raises_error(self) -> None:
        """Test initialization without config_path or config_dict raises ValueError."""
        from ai.config_loader import AIConfigLoader

        with pytest.raises(ValueError, match="Either config_path or config_dict must be provided"):
            AIConfigLoader()

    def test_init_with_nonexistent_file_raises_error(self, tmp_path: Path) -> None:
        """Test initialization with non-existent file raises FileNotFoundError."""
        from ai.config_loader import AIConfigLoader

        nonexistent_path = tmp_path / "nonexistent.yaml"
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            AIConfigLoader(config_path=nonexistent_path)


class TestEnvVarSubstitution:
    """Test environment variable substitution."""

    def test_env_var_substitution_in_string(self, config_with_env_vars: dict, mock_env_var: None) -> None:
        """Test environment variable substitution in string values."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=config_with_env_vars)
        llm_config = loader._config["llms"]["gpt4"]
        assert llm_config["api_key"] == "sk-test-12345"

    def test_env_var_not_set_remains_unchanged(self) -> None:
        """Test that unset env vars remain unchanged."""
        from ai.config_loader import AIConfigLoader

        config = {
            "llms": {
                "test": {
                    "type": "litellm",
                    "api_key": "${UNSET_VAR}",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        assert loader._config["llms"]["test"]["api_key"] == "${UNSET_VAR}"

    def test_env_var_substitution_in_nested_dicts(self, mock_env_var: None) -> None:
        """Test env var substitution works in nested dicts."""
        from ai.config_loader import AIConfigLoader

        config = {
            "level1": {
                "level2": {
                    "level3": {
                        "key": "${TEST_API_KEY}",
                    }
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        assert loader._config["level1"]["level2"]["level3"]["key"] == "sk-test-12345"

    def test_env_var_substitution_in_lists(self, mock_env_var: None) -> None:
        """Test env var substitution works in lists."""
        from ai.config_loader import AIConfigLoader

        config = {
            "items": ["${TEST_API_KEY}", "static_value", "${OPENAI_API_KEY}"]
        }
        loader = AIConfigLoader(config_dict=config)
        assert loader._config["items"] == ["sk-test-12345", "static_value", "sk-openai-test"]


class TestComponentCreation:
    """Test individual component creation."""

    def test_create_embedding_litellm(self, simple_config_dict: dict) -> None:
        """Test LiteLLM embedding adapter creation."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        embedding = loader.get_component("embeddings.default")
        assert embedding is not None
        assert embedding.model == "text-embedding-3-small"
        assert embedding.dimension == 1536

    def test_create_llm_litellm(self, simple_config_dict: dict) -> None:
        """Test LiteLLM adapter creation."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        llm = loader.get_component("llms.gpt4")
        assert llm is not None
        assert llm.model == "gpt-4o"

    def test_create_vector_store_faiss(self, simple_config_dict: dict) -> None:
        """Test FAISS vector store creation."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        vector_store = loader.get_component("vector_stores.faiss")
        assert vector_store is not None
        assert vector_store._dimension == 1536

    def test_unsupported_embedding_type_raises_error(self) -> None:
        """Test unsupported embedding type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "embeddings": {
                "test": {
                    "type": "unsupported",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Unsupported embedding type: unsupported"):
            loader.get_component("embeddings.test")

    def test_unsupported_llm_type_raises_error(self) -> None:
        """Test unsupported LLM type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "llms": {
                "test": {
                    "type": "unsupported",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Unsupported LLM type: unsupported"):
            loader.get_component("llms.test")

    def test_unsupported_vector_store_type_raises_error(self) -> None:
        """Test unsupported vector store type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "vector_stores": {
                "test": {
                    "type": "unsupported",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Unsupported vector store type: unsupported"):
            loader.get_component("vector_stores.test")


class TestReferenceResolution:
    """Test reference resolution between components."""

    def test_resolve_reference_vector_retriever(self, full_config_dict: dict) -> None:
        """Test vector retriever reference resolution."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=full_config_dict)
        retriever = loader.get_component("retrievers.vector")
        assert retriever is not None
        assert hasattr(retriever, "_embedding")
        assert hasattr(retriever, "_vector_store")

    def test_invalid_reference_format_raises_error(self, simple_config_dict: dict) -> None:
        """Test invalid reference format raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        with pytest.raises(ValueError, match="Invalid reference format"):
            loader.get_component("invalid_ref")

    def test_nonexistent_component_type_raises_error(self, simple_config_dict: dict) -> None:
        """Test non-existent component type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        with pytest.raises(ValueError, match="Component type not found in config: nonexistent"):
            loader.get_component("nonexistent.component")

    def test_nonexistent_component_name_raises_error(self, simple_config_dict: dict) -> None:
        """Test non-existent component name raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        with pytest.raises(ValueError, match="Component not found: llms.nonexistent"):
            loader.get_component("llms.nonexistent")

    def test_missing_embedding_ref_raises_error(self) -> None:
        """Test missing embedding_ref in vector retriever raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "vector": {
                    "type": "vector",
                    "vector_store_ref": "vector_stores.faiss",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="embedding_ref is required for vector retriever"):
            loader.get_component("retrievers.vector")

    def test_missing_vector_store_ref_raises_error(self) -> None:
        """Test missing vector_store_ref in vector retriever raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "vector": {
                    "type": "vector",
                    "embedding_ref": "embeddings.default",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="vector_store_ref is required for vector retriever"):
            loader.get_component("retrievers.vector")


class TestComponentCaching:
    """Test component caching prevents duplicate instantiation."""

    def test_component_cached_on_second_access(self, full_config_dict: dict) -> None:
        """Test component is cached and reused on second access."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=full_config_dict)
        
        # First access
        embedding1 = loader.get_component("embeddings.default")
        
        # Second access should return same instance
        embedding2 = loader.get_component("embeddings.default")
        
        assert embedding1 is embedding2

    def test_clear_cache_removes_cached_components(self, full_config_dict: dict) -> None:
        """Test clear_cache removes cached components."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=full_config_dict)
        
        # Create and cache a component
        embedding1 = loader.get_component("embeddings.default")
        
        # Clear cache
        loader.clear_cache()
        
        # Next access should create a new instance
        embedding2 = loader.get_component("embeddings.default")
        
        # Should be different instances (cache was cleared)
        assert embedding1 is not embedding2


class TestPipelineCreation:
    """Test pipeline creation from config."""

    def test_create_self_crag_pipeline(self, full_config_dict: dict) -> None:
        """Test SelfCRAGPipeline creation."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=full_config_dict)
        pipeline = loader.create_pipeline("self_crag")
        assert pipeline is not None
        assert hasattr(pipeline, "_llm")
        assert hasattr(pipeline, "_retriever")

    def test_create_pipeline_missing_section_raises_error(self, simple_config_dict: dict) -> None:
        """Test pipeline creation without pipelines section raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        with pytest.raises(ValueError, match="No pipelines section in config"):
            loader.create_pipeline("self_crag")

    def test_create_pipeline_nonexistent_name_raises_error(self, full_config_dict: dict) -> None:
        """Test pipeline creation with non-existent name raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=full_config_dict)
        with pytest.raises(ValueError, match="Pipeline not found: nonexistent"):
            loader.create_pipeline("nonexistent")

    def test_create_pipeline_wrong_type_raises_error(self) -> None:
        """Test pipeline creation with wrong type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "pipelines": {
                "wrong": {
                    "type": "wrong_type",
                    "llm_ref": "llms.gpt4",
                    "retriever_ref": "retrievers.vector",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Pipeline type must be 'self_crag'"):
            loader.create_pipeline("wrong")

    def test_create_pipeline_missing_llm_ref_raises_error(self) -> None:
        """Test pipeline creation without llm_ref raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "pipelines": {
                "incomplete": {
                    "type": "self_crag",
                    "retriever_ref": "retrievers.vector",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="llm_ref is required for SelfCRAGPipeline"):
            loader.create_pipeline("incomplete")

    def test_create_pipeline_missing_retriever_ref_raises_error(self) -> None:
        """Test pipeline creation without retriever_ref raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "pipelines": {
                "incomplete": {
                    "type": "self_crag",
                    "llm_ref": "llms.gpt4",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="retriever_ref is required for SelfCRAGPipeline"):
            loader.create_pipeline("incomplete")


class TestWorkflowCreation:
    """Test workflow creation from config."""

    def test_create_multi_hop_workflow_minimal(self) -> None:
        """Test MultiHopWorkflow creation with minimal config."""
        from ai.config_loader import AIConfigLoader

        config = {
            "workflows": {
                "multi_hop": {
                    "type": "multi_hop",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        workflow = loader.create_workflow("multi_hop")
        assert workflow is not None
        assert workflow._kg_backend is None
        assert workflow._retriever is None
        assert workflow._max_hops == 5

    def test_create_multi_hop_workflow_with_max_hops(self) -> None:
        """Test MultiHopWorkflow creation with custom max_hops."""
        from ai.config_loader import AIConfigLoader

        config = {
            "workflows": {
                "multi_hop": {
                    "type": "multi_hop",
                    "max_hops": 3,
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        workflow = loader.create_workflow("multi_hop")
        assert workflow._max_hops == 3

    def test_create_workflow_missing_section_raises_error(self, simple_config_dict: dict) -> None:
        """Test workflow creation without workflows section raises ValueError."""
        from ai.config_loader import AIConfigLoader

        loader = AIConfigLoader(config_dict=simple_config_dict)
        with pytest.raises(ValueError, match="No workflows section in config"):
            loader.create_workflow("multi_hop")

    def test_create_workflow_nonexistent_name_raises_error(self) -> None:
        """Test workflow creation with non-existent name raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "workflows": {
                "multi_hop": {
                    "type": "multi_hop",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Workflow not found: nonexistent"):
            loader.create_workflow("nonexistent")

    def test_create_workflow_wrong_type_raises_error(self) -> None:
        """Test workflow creation with wrong type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "workflows": {
                "wrong": {
                    "type": "wrong_type",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Workflow type must be 'multi_hop'"):
            loader.create_workflow("wrong")


class TestEnsembleRetriever:
    """Test ensemble retriever creation with multiple sub-retrievers."""

    def test_create_ensemble_retriever_with_refs(self) -> None:
        """Test ensemble retriever with retriever references."""
        from ai.config_loader import AIConfigLoader

        config = {
            "embeddings": {
                "default": {
                    "type": "litellm",
                    "model": "text-embedding-3-small",
                    "dimension": 1536,
                }
            },
            "vector_stores": {
                "faiss": {
                    "type": "faiss",
                    "dimension": 1536,
                }
            },
            "retrievers": {
                "vector1": {
                    "type": "vector",
                    "embedding_ref": "embeddings.default",
                    "vector_store_ref": "vector_stores.faiss",
                },
                "vector2": {
                    "type": "vector",
                    "embedding_ref": "embeddings.default",
                    "vector_store_ref": "vector_stores.faiss",
                },
                "ensemble": {
                    "type": "ensemble",
                    "retriever_refs": [
                        {"ref": "retrievers.vector1", "weight": 0.6},
                        {"ref": "retrievers.vector2", "weight": 0.4},
                    ],
                },
            },
        }
        loader = AIConfigLoader(config_dict=config)
        ensemble = loader.get_component("retrievers.ensemble")
        assert ensemble is not None
        assert hasattr(ensemble, "_retrievers")
        assert len(ensemble._retrievers) == 2

    def test_create_ensemble_retriever_missing_refs_raises_error(self) -> None:
        """Test ensemble retriever without retriever_refs raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "ensemble": {
                    "type": "ensemble",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="retriever_refs list is required for ensemble retriever"):
            loader.get_component("retrievers.ensemble")


class TestGraphRetriever:
    """Test graph retriever creation with KG backend."""

    def test_create_graph_retriever_missing_kg_ref_raises_error(self) -> None:
        """Test graph retriever without kg_backend_ref raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "graph": {
                    "type": "graph",
                    "llm_ref": "llms.gpt4",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="kg_backend_ref is required for graph retriever"):
            loader.get_component("retrievers.graph")

    def test_create_graph_retriever_missing_llm_ref_raises_error(self) -> None:
        """Test graph retriever without llm_ref raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "graph": {
                    "type": "graph",
                    "kg_backend_ref": "knowledge_graphs.networkx",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="llm_ref is required for graph retriever"):
            loader.get_component("retrievers.graph")


class TestUnsupportedComponentTypes:
    """Test handling of unsupported component types."""

    def test_unsupported_component_type_raises_error(self, simple_config_dict: dict) -> None:
        """Test unsupported component type in reference raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {**simple_config_dict, "unsupported": {"test": {"type": "test"}}}
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Unsupported component type: unsupported"):
            loader.get_component("unsupported.test")

    def test_unsupported_retriever_type_raises_error(self) -> None:
        """Test unsupported retriever type raises ValueError."""
        from ai.config_loader import AIConfigLoader

        config = {
            "retrievers": {
                "unsupported": {
                    "type": "unsupported_type",
                }
            }
        }
        loader = AIConfigLoader(config_dict=config)
        with pytest.raises(ValueError, match="Unsupported retriever type: unsupported_type"):
            loader.get_component("retrievers.unsupported")
