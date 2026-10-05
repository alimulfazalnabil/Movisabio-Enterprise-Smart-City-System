from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class HealthcareFacility(BaseModel):
    facility_id: str
    facility_type: str # HOSPITAL, CLINIC, PHARMACY, etc.
    location: str
    emergency_capability: bool
    status: str

class FacilityCapacity(BaseModel):
    facility_id: str
    total_beds: int
    available_beds: int
    icu_available: int
    emergency_load_status: str # NORMAL, HIGH_LOAD, FULL

class AmbulanceState(BaseModel):
    ambulance_id: str
    status: str # AVAILABLE, DISPATCHED, EN_ROUTE_TO_PATIENT, AT_SCENE, TRANSPORTING, AT_FACILITY
    location: str
    destination_facility_id: Optional[str]
    eta_minutes: Optional[float]

class HeatRiskZone(BaseModel):
    zone_id: str
    temperature_celsius: float
    vulnerability_index: float
    risk_level: str # LOW, MODERATE, HIGH, EXTREME
    healthcare_load_risk: float # Probability of increased load
