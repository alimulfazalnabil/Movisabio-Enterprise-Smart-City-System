from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class OversightMode(str, enum.Enum):
    HUMAN_IN_THE_LOOP = "HUMAN_IN_THE_LOOP"
    HUMAN_ON_THE_LOOP = "HUMAN_ON_THE_LOOP"
    HUMAN_IN_COMMAND = "HUMAN_IN_COMMAND"

class OverrideEvent(BaseModel):
    override_id: str
    action_id: str
    overriding_user: str
    reason: str
    new_action: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OversightEngine:
    def __init__(self):
        self.overrides: Dict[str, OverrideEvent] = {}
        
    def record_override(self, override: OverrideEvent) -> OverrideEvent:
        self.overrides[override.override_id] = override
        return override
        
    def get_overrides_for_action(self, action_id: str) -> List[OverrideEvent]:
        return [o for o in self.overrides.values() if o.action_id == action_id]
