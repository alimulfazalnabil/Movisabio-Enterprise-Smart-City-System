from typing import Dict, List, Any
from src.network.intersection_graph import IntersectionGraph

class CorridorOptimizer:
    """
    Coordinates signal phases across multiple intersections to enable Green Waves
    and prevent queue spillbacks.
    """
    def __init__(self, topology: IntersectionGraph):
        self.topology = topology
        
    def calculate_offsets(self, flow_speed_m_s: float) -> Dict[str, float]:
        """
        Calculates theoretical green wave offsets based on distances and flow speed.
        """
        offsets = {}
        cumulative_distance = 0.0
        
        # Simple linear progression assumption for the prototype
        nodes = list(self.topology.nodes.keys())
        for i in range(len(nodes) - 1):
            dist = self.topology.get_downstream_distance(nodes[i], nodes[i+1])
            if dist:
                cumulative_distance += dist
                # Time = Distance / Speed
                offsets[nodes[i+1]] = cumulative_distance / flow_speed_m_s if flow_speed_m_s > 0 else 0
                
        offsets[nodes[0]] = 0.0 # Origin
        return offsets

    def detect_spillback_risk(self, upstream_id: str, downstream_id: str, downstream_queue_len: float) -> bool:
        """
        If downstream queue approaches the edge distance, trigger spillback protection.
        Assume 7 meters per queued vehicle.
        """
        dist = self.topology.get_downstream_distance(upstream_id, downstream_id)
        if dist is None:
            return False
            
        physical_queue_length = downstream_queue_len * 7.0
        # If queue occupies > 80% of the link
        return physical_queue_length > (dist * 0.8)
