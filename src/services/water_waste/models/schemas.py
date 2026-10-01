from enum import Enum
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel

class DataQuality(str, Enum):
    VALID = "VALID"
    MISSING = "MISSING"
    STALE = "STALE"
    INVALID = "INVALID"
    SUSPECT = "SUSPECT"
    UNKNOWN = "UNKNOWN"

class WaterAsset(BaseModel):
    asset_id: str
    tenant_id: str
    site_id: str
    asset_type: str
    geometry: dict
    status: str
    capacity: float
    criticality: str
    condition: str
    maintenance_state: str

class WaterTelemetryEvent(BaseModel):
    event_id: str
    tenant_id: str
    asset_id: str
    timestamp: datetime
    measurement_type: str
    value: float
    unit: str
    quality: DataQuality = DataQuality.UNKNOWN
    source: str
    location: dict

class FloodState(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    ELEVATED = "ELEVATED"
    HIGH_RISK = "HIGH_RISK"
    ACTIVE_FLOOD = "ACTIVE_FLOOD"
    RECOVERY = "RECOVERY"

class FloodRiskModel(BaseModel):
    region_id: str
    timestamp: datetime
    state: FloodState
    water_level_m: float
    rainfall_mm_h: float
    confidence: float
    affected_assets: List[str] = []

class WasteBinState(str, Enum):
    EMPTY = "EMPTY"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    FULL = "FULL"
    OVERFLOW_RISK = "OVERFLOW_RISK"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    UNKNOWN = "UNKNOWN"

class WasteBin(BaseModel):
    bin_id: str
    tenant_id: str
    geometry: dict
    capacity_kg: float
    waste_type: str
    state: WasteBinState = WasteBinState.UNKNOWN

class WasteRouteRecommendation(BaseModel):
    route_id: str
    vehicle_id: str
    ordered_bin_ids: List[str]
    estimated_duration_min: float
    total_expected_kg: float
