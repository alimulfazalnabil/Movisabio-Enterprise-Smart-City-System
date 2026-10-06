from typing import Dict, Any

class SafetyEngine:
    def __init__(self, config: Dict[str, Any]):
        self.min_green = config.get("min_green", 10.0)
        self.max_green = config.get("max_green", 120.0)
        self.yellow_duration = config.get("yellow_duration", 3.0)
        self.all_red_duration = config.get("all_red_duration", 2.0)

    def validate_command(self, current_state: dict, proposed_command: dict) -> dict:
        current_phase = current_state.get("phase")
        elapsed = current_state.get("elapsed", 0.0)
        
        proposed_phase = proposed_command.get("recommended_phase")
        duration = proposed_command.get("duration", 0.0)

        # Ensure minimum green
        if current_phase != proposed_phase and elapsed < self.min_green:
            return {
                "status": "REJECTED",
                "reason": f"MIN_GREEN_VIOLATION: Elapsed {elapsed} < {self.min_green}"
            }
            
        # Ensure maximum green
        if duration > self.max_green:
            return {
                "status": "REJECTED",
                "reason": f"MAX_GREEN_VIOLATION: Proposed {duration} > {self.max_green}"
            }

        return {
            "status": "VALIDATED",
            "reason": "OK"
        }
