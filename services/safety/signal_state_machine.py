import time
from services.safety.safety_rules import SafetyRules

class SignalStateMachine:
    """
    Ensures safe transition mechanics (GREEN -> YELLOW -> ALL_RED -> GREEN).
    """
    def __init__(self, config_path: str):
        self.rules = SafetyRules(config_path)
        # Default start state
        self.active_phase = "PHASE_1"
        self.active_state = "GREEN"
        self.phase_start_time = time.time()
        
    def get_state(self):
        return {
            "phase": self.active_phase,
            "state": self.active_state,
            "elapsed": time.time() - self.phase_start_time
        }
        
    def request_phase(self, requested_phase: str):
        elapsed = time.time() - self.phase_start_time
        
        # 1. Check Safety Rules (Min/Max green, etc)
        is_safe, reason = self.rules.validate_transition(self.active_phase, requested_phase, elapsed)
        
        if not is_safe:
            return {"status": "REJECTED", "reason": reason}
            
        if self.active_phase == requested_phase:
            return {"status": "ACKNOWLEDGED", "action": "EXTENDED", "reason": reason}
            
        # 2. Execute safe transition logic (In reality, this is asynchronous and sleeps)
        print(f"[State Machine] Transitioning {self.active_phase} -> YELLOW")
        self.active_state = "YELLOW"
        # time.sleep(self.rules.phases[self.active_phase]["yellow_time"])
        
        print(f"[State Machine] Transitioning {self.active_phase} -> ALL_RED")
        self.active_state = "ALL_RED"
        # time.sleep(self.rules.phases[self.active_phase]["all_red_time"])
        
        print(f"[State Machine] Transitioning {requested_phase} -> GREEN")
        self.active_phase = requested_phase
        self.active_state = "GREEN"
        self.phase_start_time = time.time()
        
        return {"status": "ACKNOWLEDGED", "action": "TRANSITIONED", "reason": reason}
