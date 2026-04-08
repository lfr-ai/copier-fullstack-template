"""Integration test for ai_config.yaml and Container template."""

from pathlib import Path

import pytest
import yaml


def test_ai_config_yaml_exists():
    """Test that ai_config.yaml exists in template."""
    config_path = Path("template/backend/config/ai_config.yaml")
    assert config_path.exists(), "ai_config.yaml not found in template/backend/config/"


def test_ai_config_yaml_is_valid():
    """Test that ai_config.yaml is valid YAML."""
    config_path = Path("template/backend/config/ai_config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    assert config is not None
    assert isinstance(config, dict)


def test_ai_config_has_required_sections():
    """Test that ai_config.yaml has all required sections."""
    config_path = Path("template/backend/config/ai_config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Verify expected sections are present
    assert "embeddings" in config
    assert "llms" in config
    assert "vector_stores" in config
    assert "knowledge_graphs" in config
    assert "retrievers" in config
    assert "pipelines" in config
    assert "workflows" in config


def test_ai_config_self_crag_pipeline():
    """Test that ai_config.yaml has Self-CRAG pipeline configuration."""
    config_path = Path("template/backend/config/ai_config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    pipelines = config.get("pipelines", {})
    assert "self_crag" in pipelines

    self_crag = pipelines["self_crag"]
    assert self_crag["type"] == "self_crag"
    assert "llm_ref" in self_crag
    assert "retriever_ref" in self_crag


def test_ai_config_deep_rag_pipeline():
    """Test that ai_config.yaml has DeepRAG pipeline configuration."""
    config_path = Path("template/backend/config/ai_config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    pipelines = config.get("pipelines", {})
    assert "deep_rag" in pipelines

    deep_rag = pipelines["deep_rag"]
    assert deep_rag["type"] == "deep_rag"
    assert "llm_ref" in deep_rag
    assert "retriever_ref" in deep_rag


def test_ai_config_reference_resolution():
    """Test that ai_config.yaml references are properly formatted."""
    config_path = Path("template/backend/config/ai_config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Check that references follow type.name pattern
    pipelines = config.get("pipelines", {})
    self_crag = pipelines.get("self_crag", {})

    llm_ref = self_crag.get("llm_ref", "")
    assert "." in llm_ref, "llm_ref should follow type.name pattern"
    assert llm_ref.startswith("llms."), "llm_ref should start with 'llms.'"

    retriever_ref = self_crag.get("retriever_ref", "")
    assert "." in retriever_ref, "retriever_ref should follow type.name pattern"
    assert retriever_ref.startswith("retrievers."), "retriever_ref should start with 'retrievers.'"


def test_container_template_has_load_ai_config():
    """Test that Container template has load_ai_config method."""
    container_path = Path("template/backend/src/{{ project_slug }}/composition/container.py.jinja")
    assert container_path.exists(), "Container template not found"

    with container_path.open("r", encoding="utf-8") as f:
        content = f.read()

    assert "def load_ai_config" in content, "load_ai_config method not found in Container"
    assert "_ai_config_loader" in content, "_ai_config_loader cache not found in Container"
    assert "AIConfigLoader" in content, "AIConfigLoader import not found in Container"
    assert "config/ai_config.yaml" in content, "Default config path not found"


def test_container_template_has_logging():
    """Test that Container template has observability logging."""
    container_path = Path("template/backend/src/{{ project_slug }}/composition/container.py.jinja")

    with container_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # Check for INFO level logging when config is loaded
    assert "logger.info" in content or "log.info" in content
    # Check for DEBUG level logging for fallback
    assert "logger.debug" in content or "log.debug" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
