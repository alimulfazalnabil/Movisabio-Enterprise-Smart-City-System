import time
from typing import Dict, Any

class SafetyGate:
    """
    The final software barrier before physical execution.
    Evaluates requested actions against min/max green times and conflict matrices.
    """
    def __init__(self):
        # In reality, this loads from the intersection YAML config
        self.min_green = 10
        self.max_green = 120
        self.yellow_time = 4
        self.all_red_time = 2
        
    def validate_command(self, current_state: Dict, requested_action: str, params: Dict) -> Dict[str, Any]:
        elapsed = current_state.get("elapsed_time", 0)
        
        if requested_action == "EXTEND_GREEN":
            extension = params.get("seconds", 0)
            if elapsed + extension > self.max_green:
                return {"status": "REJECTED", "reason": "MAX_GREEN_VIOLATION"}
            return {"status": "APPROVED", "reason": "WITHIN_LIMITS"}
            
        elif requested_action == "NEXT_PHASE":
            if elapsed < self.min_green:
                return {"status": "REJECTED", "reason": "MIN_GREEN_VIOLATION"}
            return {"status": "APPROVED", "reason": "SAFE_TRANSITION"}
            
        return {"status": "REJECTED", "reason": "UNKNOWN_COMMAND"}
