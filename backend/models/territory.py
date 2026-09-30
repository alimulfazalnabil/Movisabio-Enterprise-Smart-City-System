from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

# Multi-tenant base model
class TenantOwned(BaseModel):
    tenant_id: str

class City(TenantOwned):
    city_id: str
    name: str
    region: str
    country: str

class Intersection(TenantOwned):
    intersection_id: str
    city_id: str
    name: str
    latitude: float
    longitude: float
    controller_ip: Optional[str] = None
    status: str = "ACTIVE"

class Lane(BaseModel):
    lane_id: str
    intersection_id: str
    direction: str # N, S, E, W
    movement: str # Left, Straight, Right

class TrafficStateObservation(TenantOwned):
    intersection_id: str
    timestamp: datetime
    lane_states: Dict[str, Dict] # {"N1": {"vehicle_count": 12, "queue": 3}}
    prediction_confidence: float

class Alert(TenantOwned):
    alert_id: str
    severity: str # INFO, WARNING, CRITICAL
    message: str
    timestamp: datetime
    resolved: bool = False
