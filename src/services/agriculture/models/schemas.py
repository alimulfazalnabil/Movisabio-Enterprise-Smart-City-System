from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class GeoPoint(BaseModel):
    lat: float
    lon: float

class Field(BaseModel):
    field_id: str
    farm_id: str
    tenant_id: str
    geometry: List[GeoPoint]
    crop_type: str
    planting_date: Optional[datetime]
    harvest_date: Optional[datetime]
    area_hectares: float
    soil_type: str
    irrigation_type: str
    status: str

class CropHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    STRESSED = "STRESSED"
    DEGRADED = "DEGRADED"
    ANOMALY = "ANOMALY"
    UNKNOWN = "UNKNOWN"

class CropState(BaseModel):
    field_id: str
    crop_type: str
    growth_stage: str
    vegetation_index: float
    moisture_indicator: float
    temperature_stress: float
    health_status: CropHealthStatus = CropHealthStatus.UNKNOWN
    confidence: float
    observation_time: datetime

class FenceState(str, Enum):
    NORMAL = "NORMAL"
    APPROACHING_BOUNDARY = "APPROACHING_BOUNDARY"
    BOUNDARY_WARNING = "BOUNDARY_WARNING"
    BOUNDARY_BREACH_CANDIDATE = "BOUNDARY_BREACH_CANDIDATE"
    INTERVENTION = "INTERVENTION"
    RETURNING = "RETURNING"

class Livestock(BaseModel):
    animal_id: str
    farm_id: str
    species: str
    breed: str
    location: GeoPoint
    health_state: str
    battery_state: float
    fence_zone: str
    fence_state: FenceState = FenceState.NORMAL
    timestamp: datetime
