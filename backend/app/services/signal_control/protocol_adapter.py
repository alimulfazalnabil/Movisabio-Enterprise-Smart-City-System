from abc import ABC, abstractmethod
from typing import Dict, Any

class ControllerAdapter(ABC):
    """
    B6.3 - Controller Protocol Abstraction.
    Vendor-agnostic interface to physical signal controllers (NTCIP, etc.).
    """
    @abstractmethod
    def connect(self) -> bool:
        pass
        
    @abstractmethod
    def disconnect(self):
        pass
        
    @abstractmethod
    def health(self, intersection_id: str) -> bool:
        pass
        
    @abstractmethod
    def read_state(self, intersection_id: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def send_phase_command(self, intersection_id: str, phase: str, duration: float) -> bool:
        pass
        
    @abstractmethod
    def send_timing_command(self, intersection_id: str, plan_id: int) -> bool:
        pass
        
    @abstractmethod
    def acknowledge(self, command_id: str) -> bool:
        pass
        
    @abstractmethod
    def verify(self, intersection_id: str, command_id: str) -> bool:
        pass
        
    @abstractmethod
    def emergency_stop(self, intersection_id: str) -> bool:
        pass
