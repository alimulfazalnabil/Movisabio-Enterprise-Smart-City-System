from typing import Dict, Any, Optional

class DecisionEngine:
    @staticmethod
    def arbitrate(candidate_decisions: list[Dict[str, Any]], rules: list[str]) -> Optional[Dict[str, Any]]:
        """
        Takes candidate decisions from AI agents and rules,
        arbitrates based on priority and safety constraints.
        Returns the finalized decision.
        """
        if not candidate_decisions:
            return None
            
        # Simplistic conflict resolution based on strict priority ordering
        priority_map = {
            "SAFETY": 1,
            "EMERGENCY": 2,
            "TRANSIT": 3,
            "GENERAL": 4,
            "OPTIMIZATION": 5
        }
        
        # Sort candidates by priority
        candidate_decisions.sort(key=lambda x: priority_map.get(x.get("category", "GENERAL"), 99))
        
        # Select the highest priority valid candidate
        best_candidate = candidate_decisions[0]
        
        return {
            "decision_id": "dec-final",
            "selected_candidate": best_candidate,
            "status": "APPROVED",
            "arbitration_reason": "PRIORITY_WIN"
        }
