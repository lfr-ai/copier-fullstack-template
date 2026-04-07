"""AI configuration loader with reference resolution and component caching.

Loads AI component configurations from YAML or dict, resolves references
between components, caches instantiated components, and provides factories
for pipelines and workflows.

Example YAML structure::

    embeddings:
      default:
        type: litellm
        model: text-embedding-3-small
        dimension: 1536

    llms:
      gpt4:
        type: litellm
        model: gpt-4o
        api_key: ${OPENAI_API_KEY}

    vector_stores:
      faiss:
        type: faiss
        dimension: 1536
        persist_dir: ./data/faiss

    retrievers:
      vector:
        type: vector
        embedding_ref: embeddings.default
        vector_store_ref: vector_stores.faiss

    pipelines:
      self_crag:
        type: self_crag
        llm_ref: llms.gpt4
        retriever_ref: retrievers.vector
"""

from __future__ import annotations

import os
import re
import structlog
from pathlib import Path
from typing import Any, final, TYPE_CHECKING

import yaml
from pydantic import BaseModel, Field, field_validator

if TYPE_CHECKING:
    from core.interfaces.embedding import EmbeddingGateway
    from core.interfaces.knowledge_graph import KnowledgeGraphGateway
    from core.interfaces.llm import LLMGateway
    from core.interfaces.retriever import RetrieverGateway
    from core.interfaces.vector_store import VectorStoreGateway
    from ai.rag.self_crag_pipeline import SelfCRAGPipeline

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")


class ComponentConfig(BaseModel):
    """Base configuration for any AI component."""

    type: str = Field(..., description="Component type identifier")
    config: dict[str, Any] = Field(default_factory=dict, description="Type-specific configuration")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Ensure type is non-empty."""
        if not v:
            msg = "type must be non-empty"
            raise ValueError(msg)
        return v


class PipelineConfig(BaseModel):
    """Configuration for pipeline/workflow components."""

    type: str = Field(..., description="Pipeline type (self_crag, multi_hop)")
    llm_ref: str | None = Field(None, description="Reference to LLM component")
    retriever_ref: str | None = Field(None, description="Reference to retriever component")
    kg_backend_ref: str | None = Field(None, description="Reference to knowledge graph backend")
    max_hops: int | None = Field(None, description="Max hops for multi-hop workflow")


@final
class AIConfigLoader:
    """Load and instantiate AI components from YAML/dict configuration.

    Features:
    - Environment variable substitution: ${VAR_NAME}
    - Reference resolution: component_type.component_name
    - Component caching: prevents duplicate instantiation
    - Factory methods for each component type
    - Pydantic validation for config structure

    Args:
        config_path (str | Path | None): Path to YAML config file.
        config_dict (dict[str, Any] | None): Pre-loaded config dictionary.
    """

    __slots__ = ("_cache", "_config", "_raw_config")

    def __init__(
        self,
        *,
        config_path: str | Path | None = None,
        config_dict: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the config loader.

        Args:
            config_path (str | Path | None): Path to YAML config file.
            config_dict (dict[str, Any] | None): Pre-loaded config dictionary.

        Raises:
            ValueError: If neither config_path nor config_dict is provided.
        """
        if config_path is None and config_dict is None:
            msg = "Either config_path or config_dict must be provided"
            raise ValueError(msg)

        self._cache: dict[str, Any] = {}
        self._raw_config: dict[str, Any] = {}
        self._config: dict[str, Any] = {}

        if config_path:
            self._load_from_file(Path(config_path))
        elif config_dict:
            self._raw_config = config_dict

        # Substitute environment variables
        self._config = self._substitute_env_vars(self._raw_config)

        logger.info(
            "AIConfigLoader initialized",
            config_path=str(config_path) if config_path else None,
            sections=list(self._config.keys()),
        )

    def _load_from_file(self, path: Path) -> None:
        """Load configuration from YAML file.

        Args:
            path (Path): Path to YAML config file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
        """
        if not path.exists():
            msg = f"Config file not found: {path}"
            raise FileNotFoundError(msg)

        with path.open("r", encoding="utf-8") as f:
            self._raw_config = yaml.safe_load(f) or {}

        logger.info("Config file loaded", path=str(path), sections=list(self._raw_config.keys()))

    def _substitute_env_vars(self, obj: Any) -> Any:
        """Recursively substitute environment variables in config.

        Replaces ${VAR_NAME} with os.environ["VAR_NAME"].

        Args:
            obj (Any): Config object (dict, list, str, or primitive).

        Returns:
            Any: Config object with env vars substituted.
        """
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        if isinstance(obj, str):
            return _ENV_VAR_PATTERN.sub(lambda m: os.environ.get(m.group(1), m.group(0)), obj)
        return obj

    def _resolve_reference(self, ref: str) -> Any:
        """Resolve a reference to a component instance.

        Reference format: component_type.component_name

        Args:
            ref (str): Reference string (e.g., 'llms.gpt4', 'retrievers.vector').

        Returns:
            Any: Resolved component instance.

        Raises:
            ValueError: If reference is invalid or component doesn't exist.
        """
        parts = ref.split(".", maxsplit=1)
        if len(parts) != 2:
            msg = f"Invalid reference format: {ref} (expected 'type.name')"
            raise ValueError(msg)

        component_type, component_name = parts

        # Check cache first
        cache_key = f"{component_type}.{component_name}"
        if cache_key in self._cache:
            logger.debug("Component cache hit", ref=ref)
            return self._cache[cache_key]

        # Resolve from config
        section = self._config.get(component_type)
        if section is None:
            msg = f"Component type not found in config: {component_type}"
            raise ValueError(msg)

        component_config = section.get(component_name)
        if component_config is None:
            msg = f"Component not found: {ref}"
            raise ValueError(msg)

        # Instantiate component based on type
        if component_type == "embeddings":
            instance = self._create_embedding(component_config)
        elif component_type == "llms":
            instance = self._create_llm(component_config)
        elif component_type == "vector_stores":
            instance = self._create_vector_store(component_config)
        elif component_type == "knowledge_graphs":
            instance = self._create_knowledge_graph(component_config)
        elif component_type == "retrievers":
            instance = self._create_retriever(component_config)
        else:
            msg = f"Unsupported component type: {component_type}"
            raise ValueError(msg)

        # Cache the instance
        self._cache[cache_key] = instance
        logger.debug("Component instantiated and cached", ref=ref, type=type(instance).__name__)

        return instance

    def _create_embedding(self, config: dict[str, Any]) -> EmbeddingGateway:
        """Create an embedding adapter from config.

        Args:
            config (dict[str, Any]): Embedding configuration.

        Returns:
            EmbeddingGateway: Configured embedding adapter.

        Raises:
            ValueError: If embedding type is unsupported.
        """
        from ai.embeddings.litellm_embeddings import LiteLLMEmbeddingAdapter

        comp_type = config.get("type")
        if comp_type == "litellm":
            return LiteLLMEmbeddingAdapter.from_config(config)

        msg = f"Unsupported embedding type: {comp_type}"
        raise ValueError(msg)

    def _create_llm(self, config: dict[str, Any]) -> LLMGateway:
        """Create an LLM adapter from config.

        Args:
            config (dict[str, Any]): LLM configuration.

        Returns:
            LLMGateway: Configured LLM adapter.

        Raises:
            ValueError: If LLM type is unsupported.
        """
        from ai.llm.litellm_adapter import LiteLLMAdapter

        comp_type = config.get("type")
        if comp_type == "litellm":
            return LiteLLMAdapter.from_config(config)

        msg = f"Unsupported LLM type: {comp_type}"
        raise ValueError(msg)

    def _create_vector_store(self, config: dict[str, Any]) -> VectorStoreGateway:
        """Create a vector store from config.

        Args:
            config (dict[str, Any]): Vector store configuration.

        Returns:
            VectorStoreGateway: Configured vector store.

        Raises:
            ValueError: If vector store type is unsupported.
        """
        from ai.vector_stores.faiss_store import FaissVectorStore

        comp_type = config.get("type")
        if comp_type == "faiss":
            return FaissVectorStore.from_config(config)

        msg = f"Unsupported vector store type: {comp_type}"
        raise ValueError(msg)

    def _create_knowledge_graph(self, config: dict[str, Any]) -> KnowledgeGraphGateway:
        """Create a knowledge graph backend from config.

        Args:
            config (dict[str, Any]): Knowledge graph configuration.

        Returns:
            KnowledgeGraphGateway: Configured knowledge graph backend.

        Raises:
            ValueError: If knowledge graph type is unsupported.
        """
        comp_type = config.get("type")

        # Dynamic import to avoid circular dependencies
        if comp_type == "networkx":
            from ai.knowledge_graph.networkx_adapter import NetworkXAdapter

            return NetworkXAdapter.from_config(config)

        if comp_type == "neo4j":
            from ai.knowledge_graph.neo4j_adapter import Neo4jAdapter

            return Neo4jAdapter.from_config(config)

        msg = f"Unsupported knowledge graph type: {comp_type}"
        raise ValueError(msg)

    def _create_retriever(self, config: dict[str, Any]) -> RetrieverGateway:
        """Create a retriever from config with reference resolution.

        Args:
            config (dict[str, Any]): Retriever configuration.

        Returns:
            RetrieverGateway: Configured retriever.

        Raises:
            ValueError: If retriever type is unsupported or references are invalid.
        """
        from ai.rag.retrievers.ensemble_retriever import EnsembleRetriever
        from ai.rag.retrievers.graph_retriever import GraphRetriever
        from ai.rag.retrievers.vector_retriever import VectorRetriever

        comp_type = config.get("type")

        if comp_type == "vector":
            # Resolve references
            embedding_ref = config.get("embedding_ref")
            vector_store_ref = config.get("vector_store_ref")

            if not embedding_ref:
                msg = "embedding_ref is required for vector retriever"
                raise ValueError(msg)
            if not vector_store_ref:
                msg = "vector_store_ref is required for vector retriever"
                raise ValueError(msg)

            embedding = self._resolve_reference(embedding_ref)
            vector_store = self._resolve_reference(vector_store_ref)

            return VectorRetriever.from_config({
                "embedding": embedding,
                "vector_store": vector_store,
            })

        if comp_type == "graph":
            # Resolve references
            kg_ref = config.get("kg_backend_ref")
            llm_ref = config.get("llm_ref")

            if not kg_ref:
                msg = "kg_backend_ref is required for graph retriever"
                raise ValueError(msg)
            if not llm_ref:
                msg = "llm_ref is required for graph retriever"
                raise ValueError(msg)

            kg_backend = self._resolve_reference(kg_ref)
            llm = self._resolve_reference(llm_ref)

            depth = config.get("depth", 2)

            return GraphRetriever.from_config({
                "knowledge_graph": kg_backend,
                "llm": llm,
                "depth": depth,
            })

        if comp_type == "ensemble":
            # Resolve retriever references
            retriever_refs = config.get("retriever_refs", [])
            if not retriever_refs:
                msg = "retriever_refs list is required for ensemble retriever"
                raise ValueError(msg)

            retrievers = []
            for ref_config in retriever_refs:
                if isinstance(ref_config, dict):
                    ref = ref_config.get("ref")
                    weight = ref_config.get("weight", 1.0)
                else:
                    ref = ref_config
                    weight = 1.0

                retriever = self._resolve_reference(ref)
                retrievers.append({"retriever": retriever, "weight": weight})

            return EnsembleRetriever.from_config({"retrievers": retrievers})

        msg = f"Unsupported retriever type: {comp_type}"
        raise ValueError(msg)

    def create_pipeline(self, pipeline_name: str) -> SelfCRAGPipeline:
        """Create a SelfCRAGPipeline from config.

        Args:
            pipeline_name (str): Pipeline name in the config.

        Returns:
            SelfCRAGPipeline: Configured pipeline instance.

        Raises:
            ValueError: If pipeline doesn't exist or configuration is invalid.
        """
        from ai.rag.self_crag_pipeline import SelfCRAGPipeline

        pipelines_section = self._config.get("pipelines")
        if pipelines_section is None:
            msg = "No pipelines section in config"
            raise ValueError(msg)

        pipeline_config = pipelines_section.get(pipeline_name)
        if pipeline_config is None:
            msg = f"Pipeline not found: {pipeline_name}"
            raise ValueError(msg)

        # Validate with Pydantic
        validated = PipelineConfig(**pipeline_config)

        if validated.type != "self_crag":
            msg = f"Pipeline type must be 'self_crag', got: {validated.type}"
            raise ValueError(msg)

        if not validated.llm_ref:
            msg = "llm_ref is required for SelfCRAGPipeline"
            raise ValueError(msg)
        if not validated.retriever_ref:
            msg = "retriever_ref is required for SelfCRAGPipeline"
            raise ValueError(msg)

        # Resolve references
        llm = self._resolve_reference(validated.llm_ref)
        retriever = self._resolve_reference(validated.retriever_ref)

        logger.info(
            "SelfCRAGPipeline created",
            pipeline_name=pipeline_name,
            llm_type=type(llm).__name__,
            retriever_type=type(retriever).__name__,
        )

        return SelfCRAGPipeline(llm=llm, retriever=retriever)

    def create_workflow(self, workflow_name: str) -> Any:
        """Create a MultiHopWorkflow from config.

        Args:
            workflow_name (str): Workflow name in the config.

        Returns:
            MultiHopWorkflow: Configured workflow instance.

        Raises:
            ValueError: If workflow doesn't exist or configuration is invalid.
        """
        # Dynamic import to avoid circular dependencies
        from ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow

        workflows_section = self._config.get("workflows")
        if workflows_section is None:
            msg = "No workflows section in config"
            raise ValueError(msg)

        workflow_config = workflows_section.get(workflow_name)
        if workflow_config is None:
            msg = f"Workflow not found: {workflow_name}"
            raise ValueError(msg)

        # Validate with Pydantic
        validated = PipelineConfig(**workflow_config)

        if validated.type != "multi_hop":
            msg = f"Workflow type must be 'multi_hop', got: {validated.type}"
            raise ValueError(msg)

        # Resolve optional references
        kg_backend = None
        if validated.kg_backend_ref:
            kg_backend = self._resolve_reference(validated.kg_backend_ref)

        retriever = None
        if validated.retriever_ref:
            retriever = self._resolve_reference(validated.retriever_ref)

        max_hops = validated.max_hops or 5

        logger.info(
            "MultiHopWorkflow created",
            workflow_name=workflow_name,
            kg_backend_type=type(kg_backend).__name__ if kg_backend else None,
            retriever_type=type(retriever).__name__ if retriever else None,
            max_hops=max_hops,
        )

        return MultiHopWorkflow(
            kg_backend=kg_backend,
            retriever=retriever,
            max_hops=max_hops,
        )

    def get_component(self, ref: str) -> Any:
        """Get a component by reference (public API).

        Args:
            ref (str): Component reference (e.g., 'llms.gpt4').

        Returns:
            Any: Resolved component instance.
        """
        return self._resolve_reference(ref)

    def clear_cache(self) -> None:
        """Clear the component cache."""
        count = len(self._cache)
        self._cache.clear()
        logger.info("Component cache cleared", count=count)
