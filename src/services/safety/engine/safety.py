from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone, timedelta
from src.services.safety.models.signal import IntersectionConfig, PhaseDefinition
from src.services.safety.models.decisions import SafetyValidationResult, SafetyCheckResult
from src.services.optimization.decisions.models import OptimizationDecision

class SafetyEngine:
    """
    Evaluates Candidate Actions from the Optimization Engine against physical safety rules.
    """
    
    def __init__(self, version: str = "safety-2.0.1"):
        self.version = version

    def validate_action(
        self,
        decision: OptimizationDecision,
        intersection_config: IntersectionConfig,
        current_state: Dict[str, Any]
    ) -> SafetyValidationResult:
        
        checks = []
        status = "APPROVED"
        reason_code = None
        
        # 1. State Freshness Check
        state_ts = current_state.get('timestamp')
        if (datetime.now(timezone.utc) - state_ts).total_seconds() > 5:
            checks.append(SafetyCheckResult(name="state_freshness", result="FAIL"))
            status = "REJECTED"
            reason_code = "STALE_STATE"
        else:
            checks.append(SafetyCheckResult(name="state_freshness", result="PASS"))
            
        # 2. Controller Health
        if current_state.get('controller_health') != 'ONLINE':
            checks.append(SafetyCheckResult(name="controller_health", result="FAIL"))
            status = "REJECTED"
            reason_code = "CONTROLLER_OFFLINE"
        else:
            checks.append(SafetyCheckResult(name="controller_health", result="PASS"))
            
        # 3. Minimum/Maximum Green constraints
        current_phase_id = decision.current_phase
        phase_config = intersection_config.phases.get(current_phase_id)
        
        if phase_config:
            elapsed = current_state.get('phase_elapsed', 0)
            action_type = decision.recommended_action.type
            
            if action_type in ['TERMINATE', 'CHANGE_PHASE']:
                if elapsed < phase_config.duration.min_green:
                    checks.append(SafetyCheckResult(name="minimum_green", result="FAIL"))
                    status = "REJECTED"
                    reason_code = "MINIMUM_GREEN_NOT_REACHED"
                else:
                    checks.append(SafetyCheckResult(name="minimum_green", result="PASS"))
            elif action_type in ['EXTEND_GREEN']:
                extend_sec = decision.recommended_action.duration_seconds or 0
                if elapsed + extend_sec > phase_config.duration.max_green:
                    checks.append(SafetyCheckResult(name="maximum_green", result="FAIL"))
                    status = "REJECTED"
                    reason_code = "MAXIMUM_GREEN_EXCEEDED"
                else:
                    checks.append(SafetyCheckResult(name="maximum_green", result="PASS"))
                    
        # ... Other checks like conflict matrix, pedestrian clearance, yellow ...

        return SafetyValidationResult(
            validation_id=f"VAL-{uuid.uuid4().hex[:8].upper()}",
            decision_id=decision.optimization_id,
            status=status,
            reason_code=reason_code,
            checks=checks,
            policy_version="policy-1.5.0", # Usually injected from PolicyEngine
            safety_version=self.version,
            timestamp=datetime.now(timezone.utc)
        )
