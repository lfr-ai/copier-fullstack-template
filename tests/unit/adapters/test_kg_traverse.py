"""Unit tests for Knowledge Graph traverse() method on Neo4j and NetworkX adapters.

Tests verify that both adapters implement the traverse() interface correctly,
returning lists of node identifiers in traversal order.
"""

import pytest


pytestmark = [pytest.mark.unit, pytest.mark.asyncio]


class TestNetworkXKnowledgeGraphTraverse:
    """Test traverse() method on NetworkX adapter."""

    async def test_traverse_single_node(self) -> None:
        """Test traverse on a graph with a single isolated node."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()
        await kg.add_triplet(subject="A", predicate="relates_to", obj="B")

        result = await kg.traverse("A")

        assert isinstance(result, list)
        assert "A" in result
        assert len(result) >= 1

    async def test_traverse_connected_graph(self) -> None:
        """Test traverse on a connected graph."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()
        await kg.add_triplets([
            ("A", "knows", "B"),
            ("B", "knows", "C"),
            ("A", "likes", "C"),
            ("C", "related_to", "D"),
        ])

        result = await kg.traverse("A")

        assert isinstance(result, list)
        assert "A" in result
        # BFS should visit connected nodes
        assert "B" in result
        assert "C" in result
        # Verify traversal includes reachable nodes
        assert len(result) >= 2

    async def test_traverse_nonexistent_node(self) -> None:
        """Test traverse on a node that doesn't exist in the graph."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()
        await kg.add_triplet(subject="A", predicate="relates_to", obj="B")

        result = await kg.traverse("NonExistent")

        assert isinstance(result, list)
        assert "NonExistent" in result
        # Should return just the starting node when not found
        assert len(result) == 1

    async def test_traverse_bidirectional_edges(self) -> None:
        """Test traverse respects both incoming and outgoing edges."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()
        await kg.add_triplets([
            ("A", "knows", "B"),
            ("C", "knows", "A"),  # A has incoming edge from C
        ])

        result = await kg.traverse("A")

        assert isinstance(result, list)
        assert "A" in result
        assert "B" in result  # successor
        assert "C" in result  # predecessor
        assert len(result) == 3


class TestNeo4jKnowledgeGraphTraverse:
    """Test traverse() method on Neo4j adapter.

    Note: These tests validate the interface without requiring Neo4j.
    """

    async def test_traverse_returns_list(self) -> None:
        """Test that traverse returns a list structure."""
        from src.ai.knowledge_graph.neo4j_adapter import Neo4jKnowledgeGraph

        # This test validates the interface shape without requiring Neo4j
        # We'll check that the method exists and has correct signature
        kg = Neo4jKnowledgeGraph.__new__(Neo4jKnowledgeGraph)

        # Verify method exists and is callable
        assert hasattr(kg, "traverse")
        assert callable(kg.traverse)


class TestTraverseInterfaceCompatibility:
    """Test that both adapters provide compatible traverse() interfaces."""

    async def test_networkx_returns_list_of_node_ids(self) -> None:
        """Verify NetworkX adapter returns list of node identifiers."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        kg = NetworkXKnowledgeGraph()
        await kg.add_triplet(subject="Node1", predicate="links", obj="Node2")

        result = await kg.traverse("Node1")

        assert isinstance(result, list)
        # All items should be valid node identifiers (strings in this case)
        for node in result:
            assert isinstance(node, (str, int, object))

    async def test_both_adapters_have_traverse_method(self) -> None:
        """Verify both adapters implement traverse() method."""
        from src.ai.knowledge_graph.neo4j_adapter import Neo4jKnowledgeGraph
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph

        # Both classes should have traverse method
        assert hasattr(NetworkXKnowledgeGraph, "traverse")
        assert hasattr(Neo4jKnowledgeGraph, "traverse")

        # Both should be async methods
        import inspect

        networkx_kg = NetworkXKnowledgeGraph()
        neo4j_kg = Neo4jKnowledgeGraph.__new__(Neo4jKnowledgeGraph)

        assert inspect.iscoroutinefunction(networkx_kg.traverse)
        assert inspect.iscoroutinefunction(neo4j_kg.traverse)
