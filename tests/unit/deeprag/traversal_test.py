import unittest
from unittest.mock import Mock, patch
from core.interfaces.knowledge_graph import KnowledgeGraphBackend

class Neo4jBackend(KnowledgeGraphBackend):
    def __init__(self, connection_str: str):
        self.connection_str = connection_str

    def traverse(self, node_id):
        """Mock Neo4j traversal function."""
        return [node_id, "mock_node_1", "mock_node_2"]

class NetworkXBackend(KnowledgeGraphBackend):
    def __init__(self, graph):
        self.graph = graph

    def traverse(self, node_id):
        """Mock NetworkX traversal function."""
        return [node_id, "mock_node_a", "mock_node_b"]

class TestKnowledgeGraphTraversal(unittest.TestCase):
    def test_neo4j_traversal(self):
        backend = Neo4jBackend("bolt://localhost:7687")
        path = backend.traverse("root")
        self.assertEqual(path, ["root", "mock_node_1", "mock_node_2"])

    def test_networkx_traversal(self):
        mock_graph = Mock()
        backend = NetworkXBackend(mock_graph)
        path = backend.traverse("root")
        self.assertEqual(path, ["root", "mock_node_a", "mock_node_b"])

if __name__ == "__main__":
    unittest.main()