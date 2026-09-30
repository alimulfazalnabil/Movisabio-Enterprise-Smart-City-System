from typing import Dict, List, Optional

class IntersectionNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        # {downstream_id: distance_meters}
        self.downstream_connections: Dict[str, float] = {}

    def connect(self, downstream_node_id: str, distance: float):
        self.downstream_connections[downstream_node_id] = distance

class IntersectionGraph:
    """
    Directed graph representing the traffic corridor network topology.
    """
    def __init__(self):
        self.nodes: Dict[str, IntersectionNode] = {}
        
    def add_node(self, node_id: str):
        if node_id not in self.nodes:
            self.nodes[node_id] = IntersectionNode(node_id)
            
    def add_edge(self, upstream_id: str, downstream_id: str, distance: float):
        self.add_node(upstream_id)
        self.add_node(downstream_id)
        self.nodes[upstream_id].connect(downstream_id, distance)
        
    def get_downstream_distance(self, upstream_id: str, downstream_id: str) -> Optional[float]:
        node = self.nodes.get(upstream_id)
        if node:
            return node.downstream_connections.get(downstream_id)
        return None
