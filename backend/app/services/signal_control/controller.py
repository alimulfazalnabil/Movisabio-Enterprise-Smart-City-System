from abc import ABC, abstractmethod
from typing import Dict, Any

class SignalController(ABC):
    @abstractmethod
    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        pass
        
    @abstractmethod
    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        pass
        
    @abstractmethod
    def health_check(self, intersection_id: str) -> bool:
        pass
        
    @abstractmethod
    def emergency_stop(self, intersection_id: str) -> bool:
        pass
