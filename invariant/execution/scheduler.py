from typing import List
from ..workflow.graph import WorkflowGraph

class TopologicalScheduler:
    """Simple scheduler that respects node dependencies."""
    
    def __init__(self, graph: WorkflowGraph):
        self.graph = graph

    def get_execution_plan(self) -> List[str]:
        """Returns the topological order of node IDs."""
        return self.graph.get_topological_order()
