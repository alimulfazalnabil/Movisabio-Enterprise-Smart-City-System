from abc import ABC, abstractmethod

class SignalController(ABC):
    @abstractmethod
    def get_state(self, signal_id: str) -> dict:
        pass

    @abstractmethod
    def send_command(self, signal_id: str, command: dict) -> bool:
        pass

    @abstractmethod
    def verify_command(self, command_id: str) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass

    @abstractmethod
    def emergency_stop(self) -> bool:
        pass

class MockSignalController(SignalController):
    def __init__(self):
        self.state = {"phase": "NS_GREEN", "remaining": 30.0}
        
    def get_state(self, signal_id: str) -> dict:
        return self.state

    def send_command(self, signal_id: str, command: dict) -> bool:
        self.state["phase"] = command.get("requested_phase", self.state["phase"])
        self.state["remaining"] = command.get("duration", 30.0)
        return True

    def verify_command(self, command_id: str) -> str:
        return "ACKNOWLEDGED"

    def health_check(self) -> bool:
        return True

    def emergency_stop(self) -> bool:
        self.state["phase"] = "ALL_RED"
        return True

class SimulationAdapter:
    def __init__(self, controller: SignalController):
        self.controller = controller
        
    def sync_state(self, traffic_state: dict):
        # Update simulation with current real-world state (if using digital twin)
        pass
