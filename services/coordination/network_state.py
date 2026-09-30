from typing import Dict, Any

class NetworkStateAggregator:
    """
    Combines individual intersection states into a unified corridor view.
    """
    def __init__(self, network_id: str):
        self.network_id = network_id
        self.intersections = {}
        
    def update_intersection(self, intersection_id: str, state: Dict[str, Any]):
        self.intersections[intersection_id] = state
        
    def get_network_state(self) -> Dict[str, Any]:
        return {
            "network_id": self.network_id,
            "intersections": self.intersections
        }
