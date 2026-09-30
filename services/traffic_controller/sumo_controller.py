from services.safety.signal_state_machine import SignalStateMachine
import datetime
import uuid

class SumoController:
    """
    Implements the Traffic Controller interface for Eclipse SUMO TraCI.
    Translates MoviSabio safe actions into TraCI API calls.
    """
    def __init__(self, config_path: str, traci_client=None):
        self.intersection_id = "INT-001"
        self.state_machine = SignalStateMachine(config_path)
        self.traci_client = traci_client
        
    def get_state(self):
        return self.state_machine.get_state()
        
    def request_action(self, requested_action: str, requested_phase: str, reason: str, optimizer: str):
        cmd_id = f"CMD-{str(uuid.uuid4())[:6].upper()}"
        
        # 1. Hardware-level safety validation
        result = self.state_machine.request_phase(requested_phase)
        
        # 2. Audit Log Construction
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
        
        # 3. Apply to SUMO environment
        if audit_log["controller_status"] == "ACKNOWLEDGED":
            if self.traci_client:
                # Map logical phases to SUMO TLS programs
                phase_mapping = {"PHASE_1": 0, "PHASE_2": 2}
                if requested_phase in phase_mapping:
                    self.traci_client.set_signal_phase(self.intersection_id, phase_mapping[requested_phase])
                    
        return audit_log
