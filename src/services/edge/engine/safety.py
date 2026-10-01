from typing import Dict, Any
from src.services.edge.models.schemas import ConnectivityState, EdgePolicyCache

class EdgeSafetyEngine:
    """
    Enforces the 'Offline Safety Principle': AI cannot take unrestricted control 
    simply because cloud validation is unreachable.
    """
    
    def validate_local_action(
        self, 
        candidate_action: Dict[str, Any], 
        connectivity: ConnectivityState, 
        policy_cache: EdgePolicyCache
    ) -> bool:
        """
        Validates if an action is allowed given the current connectivity and local cached policy.
        """
        # If offline, check if local AI control is explicitly permitted by cached policy
        if connectivity in [ConnectivityState.OFFLINE, ConnectivityState.DEGRADED]:
            if not policy_cache.offline_ai_control_allowed:
                # Revert to failsafe / hardcoded schedule
                return False
                
        # Even if allowed offline, still check hard bounds
        action_type = candidate_action.get("type")
        value = candidate_action.get("value", 0)
        
        if action_type == "GREEN_EXTENSION":
            if value > policy_cache.rules.get("max_green_seconds", 60):
                return False
                
        return True
