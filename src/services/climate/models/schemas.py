from enum import Enum
from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel

class DataQuality(str, Enum):
    MEASURED = "MEASURED"
    CALCULATED = "CALCULATED"
    MODELED = "MODELED"
    ESTIMATED = "ESTIMATED"
    FORECAST = "FORECAST"
    SCENARIO = "SCENARIO"
    UNKNOWN = "UNKNOWN"

class ConfidenceLevel(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    MEDIUM_CONFIDENCE = "MEDIUM_CONFIDENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"

class EmissionFactor(BaseModel):
    factor_id: str
    source: str
    publication_date: datetime
    geographic_scope: str
    valid_from: datetime
    valid_to: Optional[datetime] = None
    unit_activity: str
    unit_emission: str
    factor_value: float
    methodology: str

class CarbonRecord(BaseModel):
    carbon_record_id: str
    tenant_id: str
    territory_id: str
    source_category: str
    source_id: str
    activity_type: str
    activity_quantity: float
    activity_unit: str
    emission_factor_id: str
    emission_factor_value: float
    emission_quantity: float
    emission_unit: str = "kgCO2e"
    calculation_method: str
    model_version: str
    data_quality: DataQuality
    confidence: ConfidenceLevel
    timestamp: datetime

class ClimateHazard(BaseModel):
    hazard_id: str
    hazard_type: str # FLOOD, HEAT, STORM
    geometry: dict
    intensity_score: float
    probability: float
    valid_time: datetime

class ExposureModel(BaseModel):
    exposure_id: str
    hazard_id: str
    exposed_asset_ids: List[str]
    vulnerability_score: float
    potential_impact_category: str

class ClimateScenario(BaseModel):
    scenario_id: str
    tenant_id: str
    name: str
    baseline_id: Optional[str]
    assumptions: Dict[str, Any]
    interventions: List[dict]
    time_horizon_years: int
    created_at: datetime
    status: str
    
class SustainabilityKPI(BaseModel):
    kpi_id: str
    category: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    baseline_value: Optional[float] = None
    target_value: Optional[float] = None
