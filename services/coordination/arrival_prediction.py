from typing import Dict, Any

class ArrivalPredictor:
    """
    Estimates when a traffic wave released from an upstream intersection
    will arrive at the downstream intersection.
    """
    def __init__(self):
        # distance in meters / assumed free-flow speed in m/s
        self.travel_time_matrix = {
            ("INT-001", "INT-002"): 500 / 13.8,  # ~36 seconds
            ("INT-002", "INT-003"): 600 / 13.8,  # ~43 seconds
            ("INT-003", "INT-004"): 450 / 13.8   # ~32 seconds
        }
        
    def predict_arrivals(self, upstream_id: str, downstream_id: str, released_volume: int) -> Dict[str, Any]:
        link = (upstream_id, downstream_id)
        travel_time = self.travel_time_matrix.get(link, 60.0)
        
        return {
            "source": upstream_id,
            "destination": downstream_id,
            "volume_expected": released_volume,
            "eta_seconds": travel_time
        }
