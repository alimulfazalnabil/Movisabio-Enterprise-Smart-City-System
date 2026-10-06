from typing import Dict, Any
from .controller import SignalController

class PhysicalController(SignalController):
    """
    Direct Physical Controller for Pilot/Production Deployments.
    Uses a vendor-specific protocol adapter.
    """
    def __init__(self, vendor_adapter):
        self.adapter = vendor_adapter
        self.executed_commands = set()

    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        return self.adapter.read_state(intersection_id)

    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        cmd_id = command.get("command_id")
        if cmd_id and cmd_id in self.executed_commands:
            return False
            
        phase = command.get("requested_phase")
        duration = command.get("duration", 30.0)
        
        success = self.adapter.send_phase_command(intersection_id, phase, duration)
        
        if success and cmd_id:
            self.executed_commands.add(cmd_id)
                
        return success

    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        return self.adapter.verify(intersection_id, command_id)

    def health_check(self, intersection_id: str) -> bool:
        return self.adapter.health(intersection_id)

    def emergency_stop(self, intersection_id: str) -> bool:
        return self.adapter.emergency_stop(intersection_id)
