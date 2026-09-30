from typing import List
from pydantic import BaseModel
import datetime

from services.perception.pipeline import TrackedVehicle

class TrafficStateOutput(BaseModel):
    intersection_id: str
    queues: dict[str, int]
    average_speed: float
    congestion_index: float
    timestamp: datetime.datetime

class TrafficStateEngine:
    def __init__(self):
        pass

    def compute_state(self, intersection_id: str, tracked_vehicles: List[TrackedVehicle]) -> TrafficStateOutput:
        """
        Computes macroscopic traffic state metrics from microscopic vehicle detections.
        """
        # Calculate queue lengths per lane
        queues = {}
        total_speed = 0.0
        speed_count = 0

        for v in tracked_vehicles:
            lane = v.lane_id or "UNKNOWN"
            if lane not in queues:
                queues[lane] = 0
            
            # Simple queue heuristic: vehicle is slow or stopped
            if v.velocity_kmh is not None and v.velocity_kmh < 5.0:
                queues[lane] += 1
            
            if v.velocity_kmh is not None:
                total_speed += v.velocity_kmh
                speed_count += 1
                
        avg_speed = (total_speed / speed_count) if speed_count > 0 else 0.0
        
        # Simple congestion index based on arbitrary speed threshold
        free_flow_speed = 50.0
        congestion_index = 1.0 - (avg_speed / free_flow_speed) if avg_speed < free_flow_speed else 0.0
        
        return TrafficStateOutput(
            intersection_id=intersection_id,
            queues=queues,
            average_speed=avg_speed,
            congestion_index=max(0.0, congestion_index),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
