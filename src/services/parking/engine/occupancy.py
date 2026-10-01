from typing import List, Dict, Any
from datetime import datetime, timezone
from src.services.parking.models.schemas import ParkingSpace, OccupancyStatus

class SensorObservation:
    def __init__(self, source: str, status: OccupancyStatus, confidence: float, timestamp: datetime):
        self.source = source
        self.status = status
        self.confidence = confidence
        self.timestamp = timestamp

class ParkingOccupancyEngine:
    """
    Fuses multiple sensor streams (CCTV, ground sensors, meters) into a single 
    canonical occupancy state for a parking space.
    """
    
    def fuse_occupancy(self, space: ParkingSpace, observations: List[SensorObservation]) -> ParkingSpace:
        if not observations:
            # Stale / unknown state
            space.status = OccupancyStatus.UNKNOWN
            space.occupancy_confidence = 0.0
            space.updated_at = datetime.now(timezone.utc)
            return space

        # Sort by confidence and recency
        # Note: A real implementation would have a more complex Bayesian or Kalman filter approach
        # For now, we take the highest confidence observation that is within a freshness window
        valid_observations = [
            obs for obs in observations 
            if (datetime.now(timezone.utc) - obs.timestamp).total_seconds() < 300 # 5 minutes
        ]
        
        if not valid_observations:
            space.status = OccupancyStatus.UNKNOWN
            space.occupancy_confidence = 0.0
            space.updated_at = datetime.now(timezone.utc)
            return space

        # Pick the most confident valid observation
        best_obs = max(valid_observations, key=lambda o: o.confidence)
        
        space.status = best_obs.status
        space.occupancy_confidence = best_obs.confidence
        space.updated_at = datetime.now(timezone.utc)
        
        return space
