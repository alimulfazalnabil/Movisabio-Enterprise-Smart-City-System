from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class BusinessEntity(BaseModel):
    business_id: str
    business_type: str # RETAIL, WHOLESALE, RESTAURANT, HOTEL, etc.
    location: str
    operating_status: str

class EconomicActivityIndicator(BaseModel):
    zone_id: str
    business_activity_score: float
    retail_activity_score: float
    mobility_score: float
    tourism_score: float
    composite_index: Optional[float] = None
    calculation_timestamp: datetime

class EconomicShockEvent(BaseModel):
    event_id: str
    shock_type: str # SUPPLY_CHAIN_FAILURE, TOURISM_SHOCK, FLOOD, etc.
    affected_zones: List[str]
    severity: str # LOW, MODERATE, HIGH, CRITICAL

class EconomicResilience(BaseModel):
    zone_id: str
    diversity_score: float
    infrastructure_score: float
    resilience_index: float
