from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class GeologicalEntity(BaseModel):
    entity_id: str
    territory_id: str
    entity_type: str # FAULT, MINERAL_DEPOSIT, AQUIFER, ROCK_UNIT
    depth_min_m: float
    depth_max_m: float
    confidence: float
    data_quality: str

class GroundwaterObservation(BaseModel):
    observation_id: str
    aquifer_id: str
    well_id: str
    water_level_m: float
    extraction_rate_m3_day: float
    salinity: float

class GroundwaterRiskState(BaseModel):
    aquifer_id: str
    risk_type: str
    state: str # NORMAL, WATCH, STRESSED, CRITICAL
    trend: str # DECLINING, STABLE, RECHARGING

class GeologicalHazardObservation(BaseModel):
    observation_id: str
    zone_id: str
    hazard_type: str # LANDSLIDE, SUBSIDENCE, SEISMIC
    severity: str
    confidence: float

class HazardRiskCandidate(BaseModel):
    zone_id: str
    hazard_type: str
    risk_level: str
    exposed_infrastructure: List[str]
