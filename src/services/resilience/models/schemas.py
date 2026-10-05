from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class HazardEvent(BaseModel):
    hazard_id: str
    hazard_type: str # FLOOD, WILDFIRE, EARTHQUAKE, CYCLONE
    status: str # ACTIVE, VERIFIED, CLOSED
    intensity: float # 0.0 to 1.0
    confidence: float

class ExposureEntity(BaseModel):
    entity_id: str
    entity_type: str # HOSPITAL, ROAD, POWER_STATION, POPULATION
    criticality: str # C0, C1, C2, C3, C4
    vulnerability_score: float # 0.0 to 1.0

class RiskAssessment(BaseModel):
    assessment_id: str
    hazard_id: str
    entity_id: str
    risk_level: str # NORMAL, WATCH, ELEVATED, HIGH, VERY_HIGH, CRITICAL
    compound_score: float

class AssetDependency(BaseModel):
    source_entity_id: str # The asset
    target_entity_id: str # What it depends on
    relationship_type: str # DEPENDS_ON, SUPPLIES
    criticality: str

class CascadingEvent(BaseModel):
    event_id: str
    root_event_id: str
    parent_entity_id: str
    impacted_entity_id: str
    severity: str
    status: str
