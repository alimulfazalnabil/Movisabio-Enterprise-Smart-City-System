from src.signal_control.protocol import SignalProtocol
from src.signal_control.safety_gate import SafetyGate
from src.signal_control.fallback import FallbackManager

class MasterSignalController:
    """
    The orchestrator that safely routes AI Optimizer decisions to the physical layer.
    MoviSabio AI -> MasterSignalController -> Safety Gate -> Physical Hardware
    """
    def __init__(self, physical_adapter: SignalProtocol):
        self.hardware = physical_adapter
        self.safety_gate = SafetyGate()
        self.fallback = FallbackManager(self.hardware)
        
    def execute_ai_command(self, action: str, params: dict):
        if self.fallback.is_active:
            return {"status": "REJECTED", "reason": "FALLBACK_ACTIVE"}
            
        current_state = self.hardware.get_signal_state()
        
        # Pass 1: Strict Safety Validation
        safety_check = self.safety_gate.validate_command(current_state, action, params)
        if safety_check["status"] == "REJECTED":
            return safety_check
            
        # Pass 2: Hardware Execution
        try:
            if action == "EXTEND_GREEN":
                success = self.hardware.extend_phase(params.get("seconds", 0))
            elif action == "NEXT_PHASE":
                success = self.hardware.request_phase_change(params.get("phase"))
            else:
                success = False
                
            return {"status": "EXECUTED" if success else "HARDWARE_REJECTED", "reason": "OK"}
        except Exception as e:
            # Pass 3: Hard Fallback on Network/Hardware Failure
            self.fallback.trigger_fallback(f"Hardware execution error: {str(e)}")
            return {"status": "FAILED", "reason": "TRIGGERED_FALLBACK"}
