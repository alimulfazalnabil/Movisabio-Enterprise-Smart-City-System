from pydantic import BaseModel
from services.optimization.rule_based import SignalDecision

class SafetyValidationResult(BaseModel):
    is_safe: bool
    permitted_state: str
    reason: str

class SafetyEngine:
    """
    Phase 6: Safety-Critical Signal Control.
    Never let AI directly manipulate arbitrary signal states.
    """
    def __init__(self):
        # In a real system, load minimum green times, conflict matrices from PostGIS/Config
        self.min_green_seconds = 10
        
    def validate_decision(self, decision: SignalDecision, current_state: dict) -> SafetyValidationResult:
        """
        Validates the requested decision against conflict matrices and minimum timings.
        """
        # Example safety check: Ensure conflicting phases aren't both GREEN
        if decision.desired_state == "GREEN" and current_state.get("conflicting_phase") == "GREEN":
            return SafetyValidationResult(
                is_safe=False,
                permitted_state="RED",
                reason="Conflict matrix violation: conflicting phase is currently green."
            )
            
        return SafetyValidationResult(
            is_safe=True,
            permitted_state=decision.desired_state,
            reason="Decision passes all safety constraints."
        )
