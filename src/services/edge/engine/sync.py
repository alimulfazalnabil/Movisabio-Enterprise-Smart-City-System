from typing import List, Dict, Any
from datetime import datetime, timezone
from src.services.edge.models.schemas import EdgeEvent, ConnectivityState

class StoreAndForwardSync:
    """
    Manages local event buffering and cloud synchronization when connectivity recovers.
    """
    
    def __init__(self):
        self.local_event_store: List[EdgeEvent] = []
        self.current_state = ConnectivityState.ONLINE
        
    def buffer_event(self, event: EdgeEvent):
        self.local_event_store.append(event)
        
    def set_connectivity(self, state: ConnectivityState):
        self.current_state = state
        if state == ConnectivityState.RECOVERING or state == ConnectivityState.ONLINE:
            self._attempt_sync()
            
    def _attempt_sync(self):
        """
        Attempts to push pending events to cloud. Clears buffer on success.
        """
        if not self.local_event_store:
            return
            
        # In reality, this sends HTTP/MQTT requests to the cloud
        # For mock, we'll mark as synced and remove
        for event in self.local_event_store:
            event.sync_status = "SYNCED"
            
        self.local_event_store.clear()
        
    def resolve_state_conflict(self, edge_state: Dict[str, Any], cloud_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolves conflicts using domain-specific deterministic rules rather than last-write-wins.
        """
        # E.g. Safety/Emergency > Authorized Local > Cloud > History
        edge_priority = edge_state.get("priority", 0)
        cloud_priority = cloud_state.get("priority", 0)
        
        if edge_priority >= cloud_priority:
            return edge_state
        return cloud_state
