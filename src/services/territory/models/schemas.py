from enum import Enum
from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel

class SpatialDataset(BaseModel):
    dataset_id: str
    tenant_id: str
    source: str
    provider: str
    acquisition_date: datetime
    crs: str
    method: str
    data_quality: str

class Parcel(BaseModel):
    parcel_id: str
    tenant_id: str
    geometry: dict
    area_sqm: float
    land_use: str
    land_cover: str
    development_status: str
    infrastructure_access: Dict[str, str]
    risk_exposure: Dict[str, str]

class Building(BaseModel):
    building_id: str
    parcel_id: str
    geometry: dict
    height_m: float
    floors: int
    footprint_sqm: float
    approx_floor_area_sqm: float
    usage_type: str
    construction_status: str

class ConstraintLevel(str, Enum):
    CONSTRAINT = "CONSTRAINT"
    WARNING = "WARNING"
    INFORMATION = "INFORMATION"
    UNKNOWN = "UNKNOWN"

class PlanningConstraint(BaseModel):
    constraint_id: str
    parcel_id: str
    constraint_type: str # FLOOD_RISK, PROTECTED_AREA
    level: ConstraintLevel
    description: str
    policy_reference: str

class DevelopmentScenario(BaseModel):
    scenario_id: str
    tenant_id: str
    name: str
    parcel_ids: List[str]
    proposed_buildings: List[dict]
    estimated_population: int
    estimated_water_demand_lpd: float
    estimated_energy_demand_kwh: float
    estimated_trip_generation: int
