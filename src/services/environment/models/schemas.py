from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class DataQuality(str, Enum):
    VALID = "VALID"
    SUSPECT = "SUSPECT"
    STALE = "STALE"
    INVALID = "INVALID"
    MISSING = "MISSING"
    CALIBRATION_REQUIRED = "CALIBRATION_REQUIRED"
    UNKNOWN = "UNKNOWN"

class GeoPoint(BaseModel):
    lat: float
    lon: float

class EnvironmentalObservation(BaseModel):
    observation_id: str
    tenant_id: str
    site_id: str
    sensor_id: str
    parameter: str # e.g., 'PM2.5', 'temperature', 'rainfall'
    value: float
    unit: str
    location: Optional[GeoPoint] = None
    timestamp: datetime
    quality: DataQuality = DataQuality.UNKNOWN
    confidence: float
    source: str
    calibration_version: Optional[str] = None
    provenance: Optional[Dict[str, Any]] = None

class RiskType(str, Enum):
    AIR_QUALITY = "AIR_QUALITY"
    FLOOD = "FLOOD"
    HEAT = "HEAT"
    STORM = "STORM"
    NOISE = "NOISE"
    VISIBILITY = "VISIBILITY"
    ENVIRONMENTAL_SENSOR = "ENVIRONMENTAL_SENSOR"

class EnvironmentalRisk(BaseModel):
    risk_id: str
    tenant_id: str
    territory_id: str
    risk_type: RiskType
    severity: str # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    probability: float
    spatial_extent: Optional[List[GeoPoint]] = None
    temporal_window: Optional[str] = None
    evidence: List[str]
    confidence: float
    model_version: str
    status: str
