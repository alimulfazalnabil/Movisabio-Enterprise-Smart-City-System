from typing import Dict, Any
from .controller import SignalController

class MockSignalController(SignalController):
    def __init__(self):
        self.state = {"phase": "NS_GREEN", "remaining": 30.0}
        self.executed_commands = set()
        
    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        return self.state

    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        cmd_id = command.get("command_id")
        if cmd_id:
            if cmd_id in self.executed_commands:
                # Idempotent return false to indicate it was skipped
                return False
            self.executed_commands.add(cmd_id)

        self.state["phase"] = command.get("requested_phase", self.state["phase"])
        self.state["remaining"] = command.get("duration", 30.0)
        return True

    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        if command_id in self.executed_commands:
            return True
        return False

    def health_check(self, intersection_id: str) -> bool:
        return True

    def emergency_stop(self, intersection_id: str) -> bool:
        self.state["phase"] = "ALL_RED"
        return True
