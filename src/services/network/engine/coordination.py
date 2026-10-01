import uuid
from typing import Dict, List
from src.services.network.models.schemas import Corridor, SignalPlanCandidate

class CorridorCoordinator:
    """
    Generates coordinated signal offset plans for a corridor to minimize delay.
    """
    
    def generate_candidate_plan(self, corridor: Corridor, base_cycle: int, speed_mps: float, segment_lengths: Dict[str, float]) -> SignalPlanCandidate:
        """
        Simple time-space diagram progression generation for the corridor.
        """
        offsets = {}
        cumulative_offset = 0.0
        
        # Intersection 0 gets offset 0
        offsets[corridor.intersections[0]] = 0
        
        for i in range(1, len(corridor.intersections)):
            prev_int = corridor.intersections[i-1]
            curr_int = corridor.intersections[i]
            
            # Find the segment connecting them
            # For simplicity, we assume lengths are provided directly ordered by intersection
            segment_id = corridor.segments[i-1]
            length = segment_lengths.get(segment_id, 100.0)
            
            travel_time = length / speed_mps if speed_mps > 0 else 0
            cumulative_offset = (cumulative_offset + travel_time) % base_cycle
            
            offsets[curr_int] = int(cumulative_offset)
            
        return SignalPlanCandidate(
            plan_id=str(uuid.uuid4()),
            corridor_id=corridor.corridor_id,
            cycle_length_sec=base_cycle,
            offsets=offsets,
            objective_weights={"delay": 0.8, "stops": 0.2},
            predicted_delay_reduction=15.0 # Mock estimation
        )
