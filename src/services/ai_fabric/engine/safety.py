from typing import Dict, Any

class AgentSafetyGateway:
    """
    Final authorization boundary before an agent recommendation reaches physical systems.
    """
    
    def validate_candidate(self, candidate: Dict[str, Any], hard_constraints: Dict[str, Any]) -> bool:
        """
        Validates the candidate action against hard constraints.
        """
        target = candidate.get("target")
        action = candidate.get("action")
        value = candidate.get("value", 0)
        
        # Example: if action is to extend green time, check hard limits
        if action == "EXTEND_GREEN":
            max_allowed = hard_constraints.get("max_green_sec", 60)
            if value > max_allowed:
                return False
                
        return True
