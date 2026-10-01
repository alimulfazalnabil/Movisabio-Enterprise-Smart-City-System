from typing import List, Optional
from src.services.priority.models.schemas import PriorityRequest, PriorityStatus

class PriorityArbitrationEngine:
    """
    Arbitrates between multiple eligible priority requests at a single intersection.
    Returns the winning request to be submitted to the Safety Engine as a candidate action.
    """
    
    def arbitrate(self, requests: List[PriorityRequest]) -> Optional[PriorityRequest]:
        valid_requests = [r for r in requests if r.status == PriorityStatus.AUTHORIZED]
        
        if not valid_requests:
            return None
            
        # Sorting criteria:
        # 1. Priority Class (P0 > P1 > P2, etc. - lexicographical string sort works)
        # 2. Urgency (Higher is better)
        # 3. ETA (Sooner is better)
        
        # Sort in ascending order, so the "winner" is at index 0.
        # priority_class.value is 'P0', 'P1', etc.
        # -urgency makes higher urgency sort first.
        # estimated_arrival_time makes earlier times sort first.
        
        valid_requests.sort(key=lambda r: (
            r.priority_class.value, 
            -r.urgency, 
            r.estimated_arrival_time
        ))
        
        winner = valid_requests[0]
        winner.status = PriorityStatus.GRANTED
        
        # Mark others as preempted if they conflict (simplified logic here marks all as preempted)
        for req in valid_requests[1:]:
            req.status = PriorityStatus.PREEMPTED
            
        return winner
