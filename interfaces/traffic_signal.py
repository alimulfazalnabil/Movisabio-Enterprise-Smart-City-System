from abc import ABC, abstractmethod
from typing import Dict, Any

class TrafficSignalInterface(ABC):
    """
    Hardware Abstraction Layer for Traffic Controllers.
    Every controller adapter (Mock, SUMO, HIL, Physical) MUST implement this interface.
    """
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns the current signal phase and elapsed time."""
        pass
        
    @abstractmethod
    def request_phase(self, requested_phase: str, reason: str, optimizer: str) -> Dict[str, Any]:
        """Requests a standard transition to a new phase."""
        pass
        
    @abstractmethod
    def extend_phase(self, seconds: int) -> Dict[str, Any]:
        """Extends the current green phase."""
        pass
        
    @abstractmethod
    def terminate_phase(self) -> Dict[str, Any]:
        """Forces the current phase to enter yellow/red clearance immediately."""
        pass
        
    @abstractmethod
    def emergency_priority(self, route_id: str) -> Dict[str, Any]:
        """Triggers emergency preemption."""
        pass
        
    @abstractmethod
    def fail_safe(self) -> Dict[str, Any]:
        """Drops the controller into its configured hardware safe state (e.g. flashing red)."""
        pass
