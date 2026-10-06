from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class SLARisk(str, enum.Enum):
    SAFE = "SAFE"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    BREACHED = "BREACHED"

class SLAContract(BaseModel):
    contract_id: str
    service_id: str
    tenant_id: str
    required_availability: float = 99.9
    current_availability: float = 100.0
    open_incidents: int = 0
    recent_trend: float = 0.0 # positive means improving, negative degrading
    
    @property
    def risk_level(self) -> SLARisk:
        if self.current_availability < self.required_availability:
            return SLARisk.BREACHED
        
        buffer = self.current_availability - self.required_availability
        if buffer < 0.05 and self.recent_trend < 0:
            return SLARisk.HIGH
        elif buffer < 0.1:
            return SLARisk.ELEVATED
        return SLARisk.SAFE

class SLAEngine:
    def __init__(self):
        self.contracts: Dict[str, SLAContract] = {}
        
    def register_contract(self, contract: SLAContract) -> SLAContract:
        self.contracts[contract.contract_id] = contract
        return contract
        
    def evaluate_sla(self, contract_id: str, current_availability: float, open_incidents: int, trend: float) -> SLAContract:
        if contract_id not in self.contracts:
            raise ValueError("Contract not found")
        contract = self.contracts[contract_id]
        contract.current_availability = current_availability
        contract.open_incidents = open_incidents
        contract.recent_trend = trend
        return contract
