from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class Ecosystem(BaseModel):
    ecosystem_id: str
    territory_id: str
    ecosystem_type: str # FOREST, WETLAND, COASTAL, etc
    area_m2: float
    condition_status: str
    protection_status: str

class SpeciesObservation(BaseModel):
    observation_id: str
    species_id: str
    observation_method: str # CAMERA_TRAP, EDNA, SATELLITE
    confidence: float
    verification_status: str # PENDING, VERIFIED

class BiodiversityIndicator(BaseModel):
    territory_id: str
    species_richness_score: float
    habitat_diversity_score: float
    connectivity_score: float
    overall_health: str # STABLE, DEGRADED, RESTORING

class ForestChangeEvent(BaseModel):
    event_id: str
    forest_id: str
    change_type: str # CANOPY_LOSS_CANDIDATE, RESTORATION
    estimated_area_m2: float
    confidence: float
    verification_status: str

class WildfireObservation(BaseModel):
    observation_id: str
    zone_id: str
    temperature_c: float
    humidity_percent: float
    wind_speed_kmh: float
    fuel_load: str # LOW, MODERATE, HIGH, EXTREME
    smoke_detected: bool

class WildfireRiskCandidate(BaseModel):
    zone_id: str
    risk_level: str # LOW, ELEVATED, HIGH, EXTREME
    confidence: float
