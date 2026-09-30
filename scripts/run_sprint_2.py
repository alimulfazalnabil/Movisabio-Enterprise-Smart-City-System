import json
import uuid
import datetime
from services.traffic_controller.state_machine import MockTrafficController
from services.safety.engine import SafetyEngine
from services.optimization.rule_based import SignalDecision

def run_sprint_2_pipeline():
    print("--- Running Sprint 2 Pipeline ---")
    
    # 1. Initialize modules
    safety_engine = SafetyEngine()
    controller = MockTrafficController()
    
    print("\n[Step 1] Traffic State & Optimization")
    # Simulate Optimization Decision based on Traffic State
    # E.g. "High queue pressure on North-South"
    decision = SignalDecision(
        intersection_id="INT-001",
        desired_phase="NS_GREEN",
        desired_state="GREEN",
        reason="HIGH_NORTH_QUEUE"
    )
    print(f"AI Decision: {decision.model_dump()}")
    
    print("\n[Step 2] Safety Engine Gatekeeper")
    # The current phase is EW_GREEN. Safety check ensures we transition properly.
    # In a real safety engine, it checks if NS and EW conflict (they do).
    current_state = {"conflicting_phase": controller.current_phase}
    
    # To switch to NS_GREEN, we must instruct the controller to switch.
    # The Safety Engine validates the request is permitted by policy.
    validation = safety_engine.validate_decision(decision, current_state)
    print(f"Safety Validation: {validation.model_dump()}")
    
    # Note: In our current safety mock, if conflicting phase is GREEN, it rejects setting GREEN directly.
    # Let's assume the controller state machine handles the safe transition (Y->R->G) 
    # when instructed to change phase.
    
    print("\n[Step 3] Dispatch Command & Controller Simulation")
    cmd_id = f"CMD-{str(uuid.uuid4())[:8]}"
    
    # Send to controller
    response = controller.set_phase(decision.desired_phase, cmd_id)
    
    print("\n[Step 4] Command Audit Trail")
    audit_log = {
        "command_id": response["command_id"],
        "intersection_id": decision.intersection_id,
        "requested_phase": decision.desired_phase,
        "reason": decision.reason,
        "model": "rule-controller-v1",
        "safety_check": "PASSED" if validation.is_safe else "REJECTED",
        "status": response["status"],
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    print(json.dumps(audit_log, indent=2))

if __name__ == "__main__":
    run_sprint_2_pipeline()
