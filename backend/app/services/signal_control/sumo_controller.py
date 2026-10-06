from typing import Dict, Any
from .controller import SignalController
from backend.app.simulation.adapters import SUMOAdapter

class SUMOController(SignalController):
    def __init__(self, sumo_adapter: SUMOAdapter):
        self.sumo = sumo_adapter
        self.state = {"phase": "NS_GREEN", "remaining": 30.0}
        self.executed_commands = set()
        
    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        return self.state

    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        cmd_id = command.get("command_id")
        if cmd_id and cmd_id in self.executed_commands:
            return False # Idempotent rejection
            
        phase = command.get("requested_phase", self.state["phase"])
        duration = command.get("duration", 30.0)
        
        # Dispatch to SUMO world
        self.sumo.set_signal_state(intersection_id, phase, duration)
        
        self.state["phase"] = phase
        self.state["remaining"] = duration
        if cmd_id:
            self.executed_commands.add(cmd_id)
        return True

    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        return command_id in self.executed_commands

    def health_check(self, intersection_id: str) -> bool:
        return True

    def emergency_stop(self, intersection_id: str) -> bool:
        self.sumo.set_signal_state(intersection_id, "ALL_RED", 999.0)
        self.state["phase"] = "ALL_RED"
        return True
