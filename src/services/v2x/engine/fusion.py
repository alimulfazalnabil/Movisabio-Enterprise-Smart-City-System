from typing import List
from datetime import datetime, timezone
from src.services.v2x.models.schemas import CooperativeObject

class CooperativePerceptionEngine:
    """
    Fuses observations from multiple sources into CooperativeObjects.
    """
    
    def fuse_observations(self, object_id: str, observations: List[dict]) -> CooperativeObject:
        """
        Takes raw observations of the same object and fuses them (e.g., averging position/speed).
        Increases confidence based on the number of independent sources.
        """
        if not observations:
            raise ValueError("No observations provided")
            
        sources = list(set([obs["source"] for obs in observations]))
        
        # Base confidence calculation
        confidence = min(0.99, 0.5 + (len(sources) * 0.15))
        
        # Simple averaging fusion for mock
        avg_lat = sum(obs["lat"] for obs in observations) / len(observations)
        avg_lon = sum(obs["lon"] for obs in observations) / len(observations)
        avg_speed = sum(obs["speed"] for obs in observations) / len(observations)
        
        return CooperativeObject(
            object_id=object_id,
            object_type="VEHICLE", # Simplified
            position={"latitude": avg_lat, "longitude": avg_lon},
            velocity_mps=avg_speed,
            heading_deg=0.0, # Simplified
            sources=sources,
            confidence=confidence,
            state="MOVING" if avg_speed > 0.5 else "STOPPED",
            last_updated=datetime.now(timezone.utc)
        )
