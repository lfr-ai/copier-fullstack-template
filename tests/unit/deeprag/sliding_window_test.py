import unittest
from core.interfaces.knowledge_graph import SlidingWindowKnowledgeGraph

class TestSlidingWindowKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        self.window_size = 5
        self.graph = SlidingWindowKnowledgeGraph(window_size=self.window_size)

    def test_sliding_window_with_full_traversal(self):
        """
        Test that the sliding window correctly truncates a longer traversal path.
        """
        result = self.graph.traverse("any-node-id")
        self.assertEqual(len(result), self.window_size)
        self.assertEqual(result, ["Node-16", "Node-17", "Node-18", "Node-19", "Node-20"])

    def test_sliding_window_with_short_traversal(self):
        """
        Test that the sliding window does not modify a shorter traversal path.
        """
        self.graph.simulate_graph_traversal = lambda _: ["Node-1", "Node-2", "Node-3"]  # Mock shorter path
        result = self.graph.traverse("any-node-id")
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ["Node-1", "Node-2", "Node-3"])

if __name__ == "__main__":
    unittest.main()