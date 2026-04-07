from abc import ABC, abstractmethod
from typing import Any, List

class KnowledgeGraphBackend(ABC):
    @abstractmethod
    def traverse(self, node_id: Any) -> List[Any]:
        """
        Traverse the knowledge graph starting from the specified node.

        Args:
            node_id (Any): The starting node identifier.

        Returns:
            List[Any]: A list representing the path of node traversals.
        """
        pass