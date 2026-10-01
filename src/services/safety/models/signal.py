from typing import List, Dict, Optional
from pydantic import BaseModel

class SignalDuration(BaseModel):
    min_green: int
    max_green: int
    yellow: int
    all_red: int
    pedestrian_clearance: Optional[int] = None

class PhaseDefinition(BaseModel):
    phase_id: str
    name: str
    signal_groups: List[str]
    duration: SignalDuration

class SignalGroupConfig(BaseModel):
    group_id: str
    movement_type: str # e.g. 'VEHICLE', 'PEDESTRIAN'
    conflicts_with: List[str]
    
class IntersectionConfig(BaseModel):
    intersection_id: str
    signal_groups: Dict[str, SignalGroupConfig]
    phases: Dict[str, PhaseDefinition]
