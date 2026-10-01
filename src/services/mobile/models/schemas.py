from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class MobileAsset(BaseModel):
    asset_id: str
    tenant_id: str
    asset_type: str # DRONE, AUTONOMOUS_VEHICLE, EMERGENCY_VEHICLE, etc.
    status: str # AVAILABLE, ON_MISSION, MAINTENANCE, etc.
    capabilities: List[str]
    battery_state: float
    connectivity_state: str

class AssetTelemetry(BaseModel):
    asset_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    speed: float
    heading: float
    battery: float
    gps_quality: str # VALID, SUSPECT, STALE, INVALID
    
class GeofenceZone(BaseModel):
    zone_id: str
    zone_type: str # ALLOWED, RESTRICTED, PROHIBITED
    geometry: Dict[str, Any] # GeoJSON
    altitude_limits: Optional[Dict[str, float]] = None # min, max
    speed_limit: Optional[float] = None

class MissionPackage(BaseModel):
    mission_id: str
    asset_id: str
    mission_type: str
    priority: str
    status: str # PLANNING, AUTHORIZED, ACTIVE, COMPLETED, ABORTED
    waypoints: List[Dict[str, float]]
    geofence: GeofenceZone
    safety_policy: Dict[str, Any]
    abort_conditions: List[str]
    authorization_required: bool
