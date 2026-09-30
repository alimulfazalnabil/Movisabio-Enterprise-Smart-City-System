from services.safety.signal_state_machine import SignalStateMachine
import uuid
import datetime

class TrafficSignalController:
    """
    Mock Controller acting as the physical traffic light hardware interface.
    """
    def __init__(self, config_path: str):
        self.intersection_id = "INT-001"
        self.state_machine = SignalStateMachine(config_path)
        
    def get_state(self):
        return self.state_machine.get_state()
        
    def request_action(self, requested_action: str, requested_phase: str, reason: str, optimizer: str):
        # Hardware-level request simulation
        cmd_id = f"CMD-{str(uuid.uuid4())[:6].upper()}"
        
        # Route through the hardware's internal safety gatekeeper (State Machine)
        result = self.state_machine.request_phase(requested_phase)
        
        # Construct the exact audit log expected
        audit_log = {
            "command_id": cmd_id,
            "intersection_id": self.intersection_id,
            "requested_action": requested_action,
            "requested_phase": requested_phase,
            "reason": reason,
            "optimizer": optimizer,
            "safety_status": "APPROVED" if result["status"] == "ACKNOWLEDGED" else "REJECTED",
            "controller_status": result["status"],
            "controller_reason": result.get("reason", ""),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        return audit_log
