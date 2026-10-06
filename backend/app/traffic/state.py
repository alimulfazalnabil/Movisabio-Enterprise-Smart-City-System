from datetime import datetime, timezone
from backend.app.models.traffic import TrafficStateEnum
from typing import Dict, List
from backend.app.traffic.perception import Track
from backend.app.traffic.lane_logic import LaneManager
from backend.app.traffic.speed import SpeedEstimator

class TrafficStateAggregator:
    def __init__(self, lane_manager: LaneManager, speed_estimator: SpeedEstimator):
        self.lane_manager = lane_manager
        self.speed_estimator = speed_estimator

    def aggregate(self, intersection_id: str, tracks: List[Track]) -> dict:
        lane_stats = self.lane_manager.process_tracks(tracks)
        
        # Calculate speeds
        track_speeds = []
        for track in tracks:
            spd = self.speed_estimator.estimate_speed(track)
            if spd > 0:
                track_speeds.append(spd)
                
        avg_speed = sum(track_speeds) / len(track_speeds) if track_speeds else 0.0
        total_vehicles = len(tracks)
        
        # Derive congestion level
        if avg_speed < 10.0 and total_vehicles > 20:
            congestion = TrafficStateEnum.SEVERE
        elif avg_speed < 20.0 and total_vehicles > 10:
            congestion = TrafficStateEnum.HEAVY
        elif avg_speed < 40.0:
            congestion = TrafficStateEnum.MODERATE
        elif total_vehicles > 0:
            congestion = TrafficStateEnum.LIGHT
        elif total_vehicles == 0:
            congestion = TrafficStateEnum.FREE
        else:
            congestion = TrafficStateEnum.UNKNOWN
            
        return {
            "intersection_id": intersection_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "vehicle_count": total_vehicles,
            "flow": float(sum([l["flow_count"] for l in lane_stats.values()])),
            "average_speed": avg_speed,
            "occupancy": 0.0, # Not strictly calculated yet without full bounding box intersection areas
            "queue_length": 0.0,
            "density": 0.0,
            "congestion_level": congestion.value,
            "data_quality": "VALID",
            "lane_states": lane_stats
        }
