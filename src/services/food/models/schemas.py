from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class CropProduction(BaseModel):
    field_id: str
    crop_type: str
    estimated_yield: float
    production_state: str # PLANNED, GROWING, HARVEST_READY, HARVESTED

class CatchRecord(BaseModel):
    record_id: str
    vessel_id: str
    species_code: str
    catch_quantity: float
    landing_site_id: str

class ColdChainObservation(BaseModel):
    observation_id: str
    unit_id: str
    temperature_c: float
    humidity_percent: float
    expected_range_min: float
    expected_range_max: float
    door_open: bool

class FoodSecurityRisk(BaseModel):
    territory_id: str
    availability_score: float
    access_score: float
    utilization_score: float
    stability_score: float
    risk_level: str # LOW, MODERATE, HIGH, CRITICAL

class FoodBatch(BaseModel):
    batch_id: str
    product_type: str
    quantity: float
    quality_status: str
