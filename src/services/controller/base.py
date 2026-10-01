from typing import Any, Dict
from abc import ABC, abstractmethod

class TrafficController(ABC):
    """
    Abstract Base Class for interacting with Traffic Signal Controllers.
    Ensures optimization logic is decoupled from specific physical hardware (Vendor A, Vendor B)
    or simulation environments (SUMO).
    """
    
    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """Fetch current hardware state (phases, active green, health)."""
        pass
        
    @abstractmethod
    async def validate_command(self, command: Dict[str, Any]) -> bool:
        """Check if a command is structurally valid before sending."""
        pass
        
    @abstractmethod
    async def send_command(self, command: Dict[str, Any]) -> bool:
        """Issue a physical or simulated command to the controller."""
        pass
        
    @abstractmethod
    async def get_health(self) -> Dict[str, Any]:
        """Check controller hardware health."""
        pass
