from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class SovereigntyZone(BaseModel):
    zone_id: str
    geography: str
    data_residency_required: bool = True
    operational_authority: str
    retention_policy_days: int = 365
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SovereigntyEngine:
    def __init__(self):
        self.zones: Dict[str, SovereigntyZone] = {}
        
    def register_zone(self, zone: SovereigntyZone) -> SovereigntyZone:
        self.zones[zone.zone_id] = zone
        return zone
        
    def check_data_transfer(self, source_zone_id: str, target_zone_id: str) -> bool:
        if source_zone_id not in self.zones:
            return False
            
        source_zone = self.zones[source_zone_id]
        if source_zone.data_residency_required and source_zone_id != target_zone_id:
            # Simple check: if data residency is required, data cannot leave the zone.
            return False
            
        return True
