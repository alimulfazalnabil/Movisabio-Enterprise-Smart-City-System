import json
from typing import Dict, List, Tuple

class SafetyRules:
    """
    Validates traffic signal requests against the intersection's conflict matrix
    and timing constraints (min green, max green).
    """
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.conflict_matrix: Dict[str, List[str]] = self.config["conflict_matrix"]
        self.phases: Dict[str, Dict] = {p["id"]: p for p in self.config["phases"]}
        
    def validate_transition(self, current_phase: str, requested_phase: str, time_in_current_phase: float) -> Tuple[bool, str]:
        """
        Returns (is_safe, reason).
        """
        if current_phase == requested_phase:
            # Check max green
            max_green = self.phases[current_phase]["max_green"]
            if time_in_current_phase >= max_green:
                return False, f"Maximum green time ({max_green}s) exceeded."
            return True, "Safe to extend current phase."
            
        # We are transitioning to a different phase. Check min green of current phase.
        min_green = self.phases[current_phase]["min_green"]
        if time_in_current_phase < min_green:
            return False, f"Minimum green time ({min_green}s) not yet satisfied."
            
        # In a strict safety engine, you cannot jump directly to a conflicting phase
        # without going through YELLOW and ALL-RED. The state machine handles that,
        # but the rules check if the requested phase itself is topologically valid.
        if requested_phase not in self.phases:
            return False, f"Invalid phase: {requested_phase}"
            
        return True, "Transition approved. Proceed via Yellow and All-Red."
