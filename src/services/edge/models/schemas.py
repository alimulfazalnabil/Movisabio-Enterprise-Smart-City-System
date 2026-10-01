from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class ConnectivityState(str, Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    RECOVERING = "RECOVERING"

class EdgeNode(BaseModel):
    node_id: str
    tenant_id: str
    territory_id: str
    connectivity_state: ConnectivityState
    health_status: str # HEALTHY, DEGRADED, CRITICAL
    last_cloud_sync: datetime
    active_policy_version: str

class EdgeDevice(BaseModel):
    device_id: str
    node_id: str
    device_type: str
    certificate_id: str
    status: str

class EdgeEvent(BaseModel):
    event_id: str
    event_type: str
    node_id: str
    payload: Dict[str, Any]
    occurred_at: datetime
    sync_status: str # PENDING, SYNCED

class EdgePolicyCache(BaseModel):
    policy_version: str
    signature: str
    expires_at: datetime
    rules: Dict[str, Any]
    offline_ai_control_allowed: bool
