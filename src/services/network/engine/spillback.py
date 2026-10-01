import uuid
from datetime import datetime, timezone
from typing import Optional
from src.services.network.models.schemas import RoadSegment, SpillbackEvent

class SpillbackPredictor:
    """
    Predicts when a queue will exceed segment storage and spill into the upstream intersection.
    """
    
    def evaluate_segment(self, segment: RoadSegment, queue_growth_mps: float) -> Optional[SpillbackEvent]:
        """
        If the queue is growing, estimates time until it exceeds segment length.
        """
        available_storage = segment.length_meters - segment.queue_length_meters
        
        if available_storage < 0:
            available_storage = 0
            
        if queue_growth_mps <= 0 and available_storage > 10:
            return None # Not growing, or plenty of space
            
        # If queue is already full, spillback is immediate
        if available_storage <= 10:
            time_to_spillback = 0.0
            prob = 1.0
        else:
            time_to_spillback = available_storage / queue_growth_mps
            
            if time_to_spillback > 300: # Beyond 5 minutes is too far out to flag a critical event
                return None
                
            prob = min(0.95, 1.0 - (time_to_spillback / 600))
            
        return SpillbackEvent(
            event_id=str(uuid.uuid4()),
            segment_id=segment.segment_id,
            spillback_probability=prob,
            affected_upstream_intersection=segment.source_intersection_id,
            estimated_time_to_spillback_sec=time_to_spillback,
            timestamp=datetime.now(timezone.utc)
        )
