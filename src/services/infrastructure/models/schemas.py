from enum import Enum
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel

class ConditionClass(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

class AssetCondition(BaseModel):
    asset_id: str
    timestamp: datetime
    condition_score: float
    condition_class: ConditionClass = ConditionClass.UNKNOWN
    evidence: List[str]
    confidence: float
    source: str
    inspection_id: Optional[str] = None
    model_version: Optional[str] = None

class InfrastructureAsset(BaseModel):
    asset_id: str
    tenant_id: str
    asset_type: str
    subtype: str
    name: str
    geometry: dict
    location: dict
    owner: str
    operator: str
    installation_date: Optional[datetime] = None
    commissioning_date: Optional[datetime] = None
    expected_life: float
    status: str
    criticality: str
    condition_score: float
    metadata: dict = {}

class FailureRisk(BaseModel):
    asset_id: str
    failure_mode: str
    probability: float
    severity: str
    risk_level: str
    prediction_window: str
    evidence: List[str]
    confidence: float
    model_version: str

class AssetDependency(BaseModel):
    source_asset_id: str
    target_asset_id: str
    dependency_type: str
    criticality: str
    direction: str
    confidence: float

class InfrastructureDefect(BaseModel):
    defect_id: str
    asset_id: str
    defect_type: str
    geometry: dict
    severity: str
    confidence: float
    evidence: List[str]
    detected_at: datetime
    verified_at: Optional[datetime] = None
    status: str
