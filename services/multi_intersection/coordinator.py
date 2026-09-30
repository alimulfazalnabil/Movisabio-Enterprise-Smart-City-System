from pydantic import BaseModel
from typing import List, Dict
from services.traffic_state.engine import TrafficStateOutput
from services.optimization.rule_based import SignalDecision

class CorridorState(BaseModel):
    corridor_id: str
    intersections: List[str]
    average_speed_kmh: float
    total_queue_length: int

class MultiIntersectionCoordinator:
    """
    Phase 9: Multi-intersection Coordinator
    Handles green wave progression, platooning, and corridor-level optimization
    rather than isolated intersection control.
    """
    def __init__(self, corridor_id: str, intersections: List[str]):
        self.corridor_id = corridor_id
        self.intersections = intersections

    def evaluate_corridor(self, traffic_states: Dict[str, TrafficStateOutput]) -> CorridorState:
        """
        Aggregates traffic state across the entire corridor.
        """
        total_speed = 0.0
        total_queues = 0
        valid_intersections = 0
        
        for intersection_id in self.intersections:
            if intersection_id in traffic_states:
                state = traffic_states[intersection_id]
                total_speed += state.average_speed
                total_queues += sum(state.queues.values())
                valid_intersections += 1
                
        avg_speed = (total_speed / valid_intersections) if valid_intersections > 0 else 0.0
        
        return CorridorState(
            corridor_id=self.corridor_id,
            intersections=self.intersections,
            average_speed_kmh=avg_speed,
            total_queue_length=total_queues
        )
        
    def generate_green_wave_offsets(self, corridor_state: CorridorState) -> Dict[str, float]:
        """
        Phase 9 logic: Calculate time offsets between intersections to allow
        a platoon of vehicles to pass through without stopping.
        """
        # Mock calculation: if average speed is 40km/h, offset depends on distance
        # For this skeleton, we return a static dictionary mapping intersection -> offset in seconds
        offsets = {}
        cumulative_offset = 0.0
        for i, intersection_id in enumerate(self.intersections):
            offsets[intersection_id] = cumulative_offset
            # Add arbitrary 15 seconds travel time to the next intersection
            cumulative_offset += 15.0 
            
        return offsets
