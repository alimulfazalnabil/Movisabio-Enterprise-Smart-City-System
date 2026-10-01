from typing import Dict
from src.services.traffic.state.models import TrafficLevel

class CongestionModel:
    """
    Evaluates raw metrics into a normalized Congestion Index (0.0 - 1.0) 
    and classifies it into a TrafficLevel state.
    """
    
    def __init__(self, version: str = "ci-v1", weights: Dict[str, float] = None):
        self.version = version
        self.weights = weights or {
            "speed": 0.30,
            "queue": 0.25,
            "density": 0.20,
            "occupancy": 0.10,
            "delay": 0.15
        }
        assert abs(sum(self.weights.values()) - 1.0) < 0.01, "Weights must sum to 1.0"
        
    def calculate_index(self, speed_degradation: float, normalized_queue: float, 
                        density: float, occupancy: float, delay: float) -> float:
        """
        Calculates the CI based on normalized inputs (0.0 to 1.0).
        """
        ci = (
            self.weights["speed"] * speed_degradation +
            self.weights["queue"] * normalized_queue +
            self.weights["density"] * density +
            self.weights["occupancy"] * occupancy +
            self.weights["delay"] * delay
        )
        return min(max(ci, 0.0), 1.0)
        
    def classify_state(self, ci: float) -> TrafficLevel:
        if ci < 0.20:
            return TrafficLevel.FREE_FLOW
        elif ci < 0.40:
            return TrafficLevel.LIGHT
        elif ci < 0.60:
            return TrafficLevel.MODERATE
        elif ci < 0.80:
            return TrafficLevel.CONGESTED
        else:
            return TrafficLevel.SEVERE
