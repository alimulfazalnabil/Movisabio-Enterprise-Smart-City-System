from typing import List, Optional
from src.services.emergency.models.schemas import EmergencyEvent, EmergencyResource

class DispatchEngine:
    """
    Matches emergency events with available resources.
    """
    
    def recommend_resources(self, event: EmergencyEvent, available_resources: List[EmergencyResource], required_capability: str) -> Optional[EmergencyResource]:
        """
        Recommends the best available resource matching the required capability.
        In a real implementation, this would involve routing / ETA logic.
        """
        if event.status not in ["VERIFIED", "CLASSIFIED", "ACTIVE", "RESPONSE_PLANNING"]:
            return None # Do not dispatch for unverified candidates
            
        candidates = [r for r in available_resources 
                     if r.status == "AVAILABLE" and required_capability in r.capability]
                     
        if not candidates:
            return None
            
        # Simplified: Return first match (In reality, sort by ETA)
        return candidates[0]
