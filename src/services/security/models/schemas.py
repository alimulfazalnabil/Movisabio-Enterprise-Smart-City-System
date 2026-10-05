from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class DeviceIdentity(BaseModel):
    device_id: str
    tenant_id: str
    device_type: str
    firmware_version: str
    security_state: str # PROVISIONING, REGISTERED, ACTIVE, DEGRADED, QUARANTINED, RECOVERY

class SecurityEvent(BaseModel):
    event_id: str
    event_type: str
    asset_id: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL
    timestamp: datetime
    confidence: float

class Threat(BaseModel):
    threat_id: str
    type: str
    severity: str
    exploitability: str

class CyberPhysicalAsset(BaseModel):
    asset_id: str
    asset_type: str
    criticality: str
    exposure: str

class ResilienceScenario(BaseModel):
    scenario_id: str
    target_asset_id: str
    failure_type: str
    expected_impact: Optional[str] = None
