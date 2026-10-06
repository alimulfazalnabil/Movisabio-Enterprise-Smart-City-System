from typing import Dict, Any, List

class IntersectionAgent:
    """B8.13 - Local Intersection Agent"""
    def __init__(self, intersection_id: str):
        self.intersection_id = intersection_id

    def compute_local_policy(self, local_state: Dict[str, Any], corridor_constraints: Dict[str, Any]) -> Dict[str, Any]:
        # Respect the constraints pushed down from the Corridor Agent
        throttle = corridor_constraints.get("throttle", False)
        if throttle:
            return {"requested_phase": "ALL_RED", "duration": 5.0}
        
        return {"requested_phase": "NS_GREEN", "duration": 30.0}

class CorridorAgent:
    """
    B8.13 - Corridor Agent
    Maintains a broader view and issues constraints to Intersection Agents.
    """
    def __init__(self, corridor_id: str, intersections: List[str]):
        self.corridor_id = corridor_id
        self.intersection_agents = {idx: IntersectionAgent(idx) for idx in intersections}

    def coordinate(self, corridor_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        # Calculate B8.8 Spillback Risk globally
        commands = {}
        for idx, agent in self.intersection_agents.items():
            constraints = {}
            # Example constraint generation based on corridor context
            risk = corridor_state.get("spillback_risks", {}).get(idx, 0.0)
            if risk > 0.8:
                constraints["throttle"] = True
                
            local_decision = agent.compute_local_policy(corridor_state.get(idx, {}), constraints)
            commands[idx] = local_decision
            
        return commands
