"""Integration tests for Self-CRAG and DeepRAG adapter wiring.

Verifies that pipelines correctly accept and use adapters via dependency injection.
Uses the actual NetworkX knowledge graph adapter and mock retriever to demonstrate
the wiring pattern.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


class TestAdapterWiring:
    """Integration tests for adapter dependency injection patterns."""

    @pytest.mark.asyncio
    async def test_multihop_workflow_accepts_kg_and_retriever(self) -> None:
        """MultiHopWorkflow should accept KG backend and retriever via constructor."""
        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph
        from src.ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow

        # Create NetworkX KG adapter
        kg_backend = NetworkXKnowledgeGraph()

        # Seed KG with test data using triplets
        await kg_backend.add_triplet(
            subject="Paris", predicate="capital_of", obj="France"
        )
        await kg_backend.add_triplet(
            subject="France", predicate="located_in", obj="Europe"
        )

        # Create workflow with KG backend (no retriever for simplicity)
        workflow = MultiHopWorkflow(
            kg_backend=kg_backend,
            retriever=None,
            max_hops=3,
        )

        # Execute multi-hop traversal
        trace = await workflow.traverse_and_enrich(start_node="Paris")

        # Verify trace structure
        assert len(trace) > 0
        assert all("node" in hop for hop in trace)
        assert all("enrichment" in hop for hop in trace)

        # Verify first hop is the starting node
        assert trace[0]["node"] == "Paris"

        # Without retriever, enrichment should be empty
        assert all(len(hop["enrichment"]) == 0 for hop in trace)

    @pytest.mark.asyncio
    async def test_multihop_workflow_logging(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """MultiHopWorkflow should log adapter selection at INFO level."""
        import logging

        from src.ai.knowledge_graph.networkx_adapter import NetworkXKnowledgeGraph
        from src.ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow

        caplog.set_level(logging.INFO)

        # Create adapters
        kg_backend = NetworkXKnowledgeGraph()
        await kg_backend.add_triplet(subject="A", predicate="connects", obj="B")

        # Create workflow (should log initialization)
        workflow = MultiHopWorkflow(
            kg_backend=kg_backend,
            retriever=None,
            max_hops=2,
        )

        # Execute (should log traversal)
        await workflow.traverse_and_enrich(start_node="A")

        # Verify INFO-level logging occurred
        log_messages = [record.message for record in caplog.records]
        assert any("MultiHopWorkflow initialized" in msg for msg in log_messages)
        assert any("Starting multi-hop traversal" in msg for msg in log_messages)
        assert any("Multi-hop traversal completed" in msg for msg in log_messages)

    @pytest.mark.asyncio
    async def test_multihop_workflow_without_kg_backend(self) -> None:
        """MultiHopWorkflow should fall back to vector-only traversal when KG unavailable."""
        from src.ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow

        # Create workflow without KG backend
        workflow = MultiHopWorkflow(
            kg_backend=None,  # No KG
            retriever=None,  # No retriever
            max_hops=3,
        )

        # Should complete with simulated vector-only traversal
        trace = await workflow.traverse_and_enrich(start_node="test_query")

        assert len(trace) > 0
        assert all("node" in hop for hop in trace)
        # Nodes should be simulated (Vector-1, Vector-2, etc.)
        assert all("Vector-" in str(hop["node"]) for hop in trace)

    @pytest.mark.asyncio
    async def test_kg_backend_protocol_contract(self) -> None:
        """Verify KnowledgeGraphBackend protocol contract is satisfied."""
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

        # Test traverse (added in T01)
        traversal = await kg.traverse(node_id="test_node")
        assert isinstance(traversal, list)
        assert len(traversal) > 0
        assert "test_node" in traversal

    @pytest.mark.asyncio
    async def test_multihop_workflow_constructor_signature(self) -> None:
        """Verify MultiHopWorkflow constructor accepts correct parameters."""
        from src.ai.langgraph_workflows.multi_hop_workflow import MultiHopWorkflow
        import inspect

        # Get constructor signature
        sig = inspect.signature(MultiHopWorkflow.__init__)
        params = list(sig.parameters.keys())

        # Verify expected parameters
        assert "self" in params
        assert "kg_backend" in params
        assert "retriever" in params
        assert "max_hops" in params

        # Verify parameter types from annotations
        annotations = MultiHopWorkflow.__init__.__annotations__
        # kg_backend should be Optional[KnowledgeGraphBackend]
        assert "kg_backend" in annotations
        # retriever should be Optional[RetrieverGateway]
        assert "retriever" in annotations
        # max_hops should be int
        assert "max_hops" in annotations
