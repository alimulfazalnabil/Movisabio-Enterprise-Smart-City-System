from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone
import enum

class ConnectivityState(str, enum.Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    LOCAL_AUTONOMY = "LOCAL_AUTONOMY"
    RECOVERING = "RECOVERING"
    SYNCHRONIZING = "SYNCHRONIZING"

class EdgeGateway(BaseModel):
    edge_site_id: str
    tenant_id: str
    connectivity_state: ConnectivityState
    last_heartbeat: datetime
    software_version: str
    configuration_version: str

    def evaluate_connectivity(self, current_time: datetime, timeout_seconds: int = 30) -> None:
        delta = (current_time - self.last_heartbeat).total_seconds()
        if delta > timeout_seconds:
            self.connectivity_state = ConnectivityState.OFFLINE
        elif delta > timeout_seconds / 2:
            self.connectivity_state = ConnectivityState.DEGRADED
        else:
            if self.connectivity_state in [ConnectivityState.OFFLINE, ConnectivityState.LOCAL_AUTONOMY]:
                self.connectivity_state = ConnectivityState.RECOVERING
            elif self.connectivity_state != ConnectivityState.SYNCHRONIZING:
                self.connectivity_state = ConnectivityState.ONLINE
