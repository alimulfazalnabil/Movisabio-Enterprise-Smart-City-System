from abc import ABC, abstractmethod
from typing import Dict, Any

class SignalProtocol(ABC):
    """
    Hardware-agnostic protocol for all traffic controllers (SUMO, NTCIP, Modbus, etc.)
    """
    @abstractmethod
    def get_current_phase(self) -> str:
        pass
        
    @abstractmethod
    def get_signal_state(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def request_phase_change(self, phase_id: str) -> bool:
        pass
        
    @abstractmethod
    def extend_phase(self, seconds: int) -> bool:
        pass
        
    @abstractmethod
    def shorten_phase(self, seconds: int) -> bool:
        pass
        
    @abstractmethod
    def get_controller_status(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def enable_ai_control(self) -> bool:
        pass
        
    @abstractmethod
    def disable_ai_control(self) -> bool:
        pass
