import logging
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow
from unittest.mock import Mock

logger = logging.getLogger("test_observability")

@pytest.fixture
def vector_store_mock():
    return Mock()

@pytest.fixture
def kg_backend_mock():
    mock = Mock()
    mock.traverse.return_value = ["Node1", "Node2", "Node3", "Node4", "Node5"]
    return mock

@pytest.fixture
def workflow(kg_backend_mock, vector_store_mock):
    return MultiHopWorkflow(kg_backend_mock, vector_store_mock, max_hops=5)

@pytest.fixture
def caplog_namespace(caplog):
    caplog.set_level(logging.DEBUG, logger="src.ai.langgraph_workflows.multi_hop_workflow")
    return caplog

def test_traverse_and_enrich_with_kg(caplog_namespace, workflow):
    start_node = "Node0"
    trace = workflow.traverse_and_enrich(start_node)

    # Verify the log messages
    assert "Using knowledge graph backend." in caplog_namespace.text
    assert "Hop 1/5: Node=Node1, Enrichment={'embedding': 'Embedding for Node1'}" in caplog_namespace.text
    assert "Completed traversal and enrichment." in caplog_namespace.text

def test_traverse_and_enrich_without_kg(caplog_namespace, vector_store_mock):
    workflow = MultiHopWorkflow(None, vector_store_mock, max_hops=5)
    start_node = "Node0"
    trace = workflow.traverse_and_enrich(start_node)

    # Verify the log messages
    assert "Knowledge graph backend unavailable. Falling back to vector-only traversal." in caplog_namespace.text
    assert "Hop 1/5: Node=Vector-1, Enrichment={'embedding': 'Embedding for Vector-1'}" in caplog_namespace.text
    assert "Completed traversal and enrichment." in caplog_namespace.text