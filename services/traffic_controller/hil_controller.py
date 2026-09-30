from typing import Dict, Any
import time
from interfaces.traffic_signal import TrafficSignalInterface
from services.safety.safety_rules import SafetyRules
from services.safety.signal_state_machine import SignalStateMachine

class HILController(TrafficSignalInterface):
    """
    Hardware-in-the-Loop Controller Adapter.
    Communicates with physical test hardware over IP/Serial while enforcing MoviSabio safety rules.
    """
    def __init__(self, config_path: str, ip_address: str = "192.168.1.100", port: int = 502):
        self.config_path = config_path
        self.ip_address = ip_address
        self.port = port
        
        # In a real system, this would establish a Modbus/NTCIP socket connection
        self.connected = False
        self._connect_to_hardware()
        
        # MoviSabio local safety barrier
        self.safety = SafetyRules(config_path)
        self.state_machine = SignalStateMachine()
        
    def _connect_to_hardware(self):
        print(f"[HIL] Attempting connection to hardware controller at {self.ip_address}:{self.port}")
        time.sleep(1) # Simulating handshake
        self.connected = True
        print("[HIL] Connection established. Hardware sync complete.")
        
    def _send_hardware_command(self, command: str, payload: Dict) -> bool:
        if not self.connected:
            raise ConnectionError("Lost connection to HIL hardware.")
        # Simulating hardware ACK
        print(f"[HIL] TX -> {command} | {payload}")
        print(f"[HIL] RX <- ACK")
        return True

    def get_status(self) -> Dict[str, Any]:
        # Querying the physical hardware state
        state = self.state_machine.get_state()
        return {
            "phase": state["current_phase"],
            "elapsed": state["elapsed_time"],
            "hardware_sync": True
        }

    def request_phase(self, requested_phase: str, reason: str, optimizer: str) -> Dict[str, Any]:
        """
        The AI proposes a phase. We validate it locally. If safe, we transmit it to the hardware.
        """
        current_state = self.state_machine.get_state()
        
        # 1. Evaluate safety constraints locally before ever touching the network
        is_safe, violation = self.safety.evaluate_request(
            current_phase=current_state["current_phase"],
            requested_phase=requested_phase,
            elapsed_time=current_state["elapsed_time"]
        )
        
        audit_log = {
            "timestamp": time.time(),
            "optimizer_source": optimizer,
            "requested_phase": requested_phase,
            "reason": reason,
            "safety_status": "APPROVED" if is_safe else "REJECTED",
            "violation": violation,
            "hardware_ack": False
        }
        
        # 2. If safe, update local state machine and transmit to hardware
        if is_safe:
            self.state_machine.transition_to(requested_phase)
            ack = self._send_hardware_command("SET_PHASE", {"phase": requested_phase})
            audit_log["hardware_ack"] = ack
            
        return audit_log

    def extend_phase(self, seconds: int) -> Dict[str, Any]:
        ack = self._send_hardware_command("EXTEND_GREEN", {"duration": seconds})
        return {"action": "extend", "ack": ack}

    def terminate_phase(self) -> Dict[str, Any]:
        ack = self._send_hardware_command("FORCE_TERMINATE", {})
        return {"action": "terminate", "ack": ack}

    def emergency_priority(self, route_id: str) -> Dict[str, Any]:
        ack = self._send_hardware_command("EMERGENCY_PREEMPT", {"route": route_id})
        return {"action": "emergency", "ack": ack}

    def fail_safe(self) -> Dict[str, Any]:
        ack = self._send_hardware_command("FAIL_SAFE_FLASH", {})
        return {"action": "fail_safe", "ack": ack}
