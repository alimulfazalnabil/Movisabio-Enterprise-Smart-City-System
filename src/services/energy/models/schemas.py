from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class EnergyAsset(BaseModel):
    asset_id: str
    territory_id: str
    asset_type: str # SOLAR_FARM, SUBSTATION, FEEDER, BATTERY, EV_CHARGER
    rated_power_kw: float
    operational_status: str

class GridCongestionState(BaseModel):
    asset_id: str
    territory_id: str
    current_load_kw: float
    rated_capacity_kw: float
    state: str # NORMAL, ELEVATED, CONSTRAINED, CONGESTED, FAILURE_RISK
    confidence: float
    time_horizon_minutes: int

class CriticalLoadAsset(BaseModel):
    asset_id: str
    asset_type: str # HOSPITAL, WATER_PUMP, TRAFFIC_CONTROL
    criticality: str # HIGH, CRITICAL
    backup_capacity_kw: float
    backup_duration_minutes: int

class GridOutage(BaseModel):
    outage_id: str
    affected_feeders: List[str]
    status: str # DETECTED, IMPACT_ASSESSED, RESTORATION, CLOSED
    affected_critical_loads: List[str]
