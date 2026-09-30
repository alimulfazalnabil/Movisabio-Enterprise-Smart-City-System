from typing import Dict, Any

class CoordinationPolicy:
    """
    Defines the rules for multi-intersection Green Waves and priorities.
    """
    def __init__(self):
        self.priority_mode = "NORMAL"
        self.green_wave_active = True
        
    def resolve_conflicts(self, local_action: str, network_requirement: str) -> str:
        if self.priority_mode == "EMERGENCY":
            return network_requirement # Override local AI
            
        if self.green_wave_active and network_requirement == "MAINTAIN_GREEN":
            # Prevent local AI from terminating green early if a platoon is arriving
            if local_action == "SWITCH_PHASE":
                return "OVERRIDE_MAINTAIN"
                
        return local_action
