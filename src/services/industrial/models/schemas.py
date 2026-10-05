from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MachineAsset(BaseModel):
    asset_id: str
    asset_type: str
    status: str # RUNNING, IDLE, DOWN
    operating_hours: float
    maintenance_interval_hours: float

class OEEData(BaseModel):
    availability: float
    performance: float
    quality: float
    overall_oee: float

class ProductionLine(BaseModel):
    line_id: str
    assets: List[MachineAsset]
    current_oee: Optional[OEEData]
    status: str

class MaintenancePrediction(BaseModel):
    asset_id: str
    rul_min_days: int
    rul_max_days: int
    confidence: float
    recommended_action: str
