import json
from typing import Dict, Any, Callable, List

class GlobalEventBus:
    """
    Decoupled event-driven architecture for the MoviSabio Territorial Platform.
    Replaces point-to-point API calls with Pub/Sub.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
    def publish(self, event_type: str, payload: Dict[str, Any]):
        """
        e.g., event_type="vehicle.detected", payload={"intersection": "INT-001"}
        """
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(payload)
                
# Singleton instance for the platform
event_bus = GlobalEventBus()
