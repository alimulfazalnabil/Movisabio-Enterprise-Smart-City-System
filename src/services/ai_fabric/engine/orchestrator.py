from typing import List, Dict, Any
from src.services.ai_fabric.models.schemas import AgentMessage, AgentRegistry

class AgentOrchestrator:
    """
    Coordinates multi-agent workflows and resolves inter-agent conflicts.
    """
    
    def resolve_conflict(self, candidate_proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Resolves conflicts using a deterministic hierarchy.
        Priority: Emergency > Critical Infrastructure > Transit > General Traffic > Environment > Normal
        """
        priority_map = {
            "EMERGENCY": 100,
            "CRITICAL_INFRASTRUCTURE": 80,
            "TRANSIT": 60,
            "TRAFFIC": 40,
            "ENVIRONMENT": 20,
            "NORMAL": 0
        }
        
        if not candidate_proposals:
            return {}
            
        # Sort by deterministic priority hierarchy
        sorted_proposals = sorted(
            candidate_proposals, 
            key=lambda x: priority_map.get(x.get("domain", "NORMAL"), 0), 
            reverse=True
        )
        
        # In a real system, we'd also check if proposals are mutually exclusive before outright overriding.
        # Here we just pick the highest priority as the 'winner'.
        winner = sorted_proposals[0]
        return winner
