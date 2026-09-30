from services.coordination.network_state import NetworkStateAggregator
from services.coordination.arrival_prediction import ArrivalPredictor
from services.coordination.coordination_policy import CoordinationPolicy
from typing import Dict, Any

class CorridorOptimizer:
    """
    Evaluates the whole corridor to produce a synchronized signal plan.
    """
    def __init__(self, network_id: str):
        self.aggregator = NetworkStateAggregator(network_id)
        self.predictor = ArrivalPredictor()
        self.policy = CoordinationPolicy()
        
    def evaluate_corridor(self, local_decisions: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Takes the raw decisions from each intersection's DQN/PPO agent,
        applies upstream arrival predictions, and issues coordinated overrides.
        """
        coordinated_actions = {}
        
        # In a real scenario, this loops through intersections geographically
        for intersection_id, decision in local_decisions.items():
            action = decision.get("requested_action", "MAINTAIN")
            
            # Example: Check if upstream is sending a wave
            if intersection_id == "INT-002":
                arrival = self.predictor.predict_arrivals("INT-001", "INT-002", 40)
                if arrival["eta_seconds"] < 15.0:
                    action = self.policy.resolve_conflicts(action, "MAINTAIN_GREEN")
                    
            coordinated_actions[intersection_id] = {
                "requested_action": action,
                "requested_phase": decision.get("requested_phase"),
                "reason": "CORRIDOR_COORDINATED" if action != decision.get("requested_action") else decision.get("reason"),
                "optimizer": "Multi-Agent-Corridor"
            }
            
        return coordinated_actions
