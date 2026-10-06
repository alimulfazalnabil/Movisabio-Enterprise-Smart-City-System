from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class StateType(str, enum.Enum):
    HISTORICAL = "HISTORICAL"
    CURRENT = "CURRENT"
    FORECAST = "FORECAST"
    SCENARIO = "SCENARIO"
    COUNTERFACTUAL = "COUNTERFACTUAL"

class TwinSnapshot(BaseModel):
    snapshot_id: str
    twin_id: str
    state_type: StateType
    timestamp: datetime
    data: Dict[str, Any]
    provenance: Optional[Dict[str, Any]] = None

class TwinStateEngine:
    def __init__(self):
        self.snapshots: Dict[str, TwinSnapshot] = {}
        
    def create_snapshot(self, twin_id: str, state_type: StateType, data: Dict[str, Any]) -> TwinSnapshot:
        snapshot = TwinSnapshot(
            snapshot_id=f"snap-{int(datetime.now().timestamp())}",
            twin_id=twin_id,
            state_type=state_type,
            timestamp=datetime.now(),
            data=data
        )
        self.snapshots[snapshot.snapshot_id] = snapshot
        return snapshot
