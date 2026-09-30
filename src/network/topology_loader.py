import json
from src.network.intersection_graph import IntersectionGraph

class TopologyLoader:
    """
    Loads corridor topology from JSON/YAML configurations.
    """
    @staticmethod
    def load_from_dict(data: dict) -> IntersectionGraph:
        graph = IntersectionGraph()
        
        # Add nodes
        for node in data.get("intersections", []):
            graph.add_node(node["id"])
            
        # Add edges
        for edge in data.get("corridors", []):
            graph.add_edge(
                edge["upstream"], 
                edge["downstream"], 
                edge["distance_m"]
            )
            
        return graph
