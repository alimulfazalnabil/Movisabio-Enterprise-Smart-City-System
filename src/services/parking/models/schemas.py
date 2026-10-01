from enum import Enum
from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class SpaceType(str, Enum):
    ON_STREET = "ON_STREET"
    OFF_STREET = "OFF_STREET"
    GARAGE = "GARAGE"
    LOT = "LOT"
    LOADING_ZONE = "LOADING_ZONE"
    DISABLED_ACCESS = "DISABLED_ACCESS"
    EV_CHARGING = "EV_CHARGING"
    TAXI = "TAXI"
    BUS_STOP = "BUS_STOP"
    MOTORCYCLE = "MOTORCYCLE"
    BICYCLE = "BICYCLE"
    EMERGENCY = "EMERGENCY"
    RESERVED = "RESERVED"

class OccupancyStatus(str, Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"
    UNKNOWN = "UNKNOWN"
    RESERVED = "RESERVED"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class GeoPoint(BaseModel):
    lat: float
    lon: float

class ParkingSpace(BaseModel):
    space_id: str
    tenant_id: str
    site_id: str
    zone_id: str
    geometry: Optional[List[GeoPoint]] = None
    space_type: SpaceType
    vehicle_type: Optional[str] = None
    status: OccupancyStatus = OccupancyStatus.UNKNOWN
    occupancy_confidence: float = 0.0
    pricing_policy: Optional[str] = None
    restrictions: List[str] = []
    sensor_id: Optional[str] = None
    camera_id: Optional[str] = None
    updated_at: datetime

class CurbStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESTRICTED = "RESTRICTED"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    UNKNOWN = "UNKNOWN"

class CurbSegment(BaseModel):
    curb_id: str
    road_id: str
    geometry: Optional[List[GeoPoint]] = None
    permitted_use: List[str]
    time_window: Optional[str] = None
    capacity: int
    restrictions: List[str]
    status: CurbStatus
