from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class AnomalyType(str, enum.Enum):
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    WORKFORCE = "WORKFORCE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    CUSTOMER = "CUSTOMER"
    STRATEGIC = "STRATEGIC"

class Anomaly(BaseModel):
    anomaly_id: str
    type: AnomalyType
    metric: str
    observed_value: float
    expected_value: float
    confidence: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Situation(BaseModel):
    situation_id: str
    name: str
    anomalies: List[str] = Field(default_factory=list)
    risk_level: str = "LOW"
    status: str = "ACTIVE"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AnomalyEngine:
    def __init__(self):
        self.anomalies: Dict[str, Anomaly] = {}
        self.situations: Dict[str, Situation] = {}
        
    def detect_anomaly(self, anomaly: Anomaly) -> Anomaly:
        self.anomalies[anomaly.anomaly_id] = anomaly
        self._correlate_situations()
        return anomaly
        
    def _correlate_situations(self):
        # Extremely simplified correlation logic for demonstration
        # E.g. Cloud Cost Up + GPU Demand Up = AI Infrastructure Risk
        active_anoms = list(self.anomalies.values())
        
        has_cost_spike = any(a.type == AnomalyType.FINANCIAL and a.metric == "cloud_cost" and a.observed_value > a.expected_value * 1.2 for a in active_anoms)
        has_gpu_demand = any(a.type == AnomalyType.INFRASTRUCTURE and a.metric == "gpu_demand" and a.observed_value > a.expected_value * 1.2 for a in active_anoms)
        
        if has_cost_spike and has_gpu_demand:
            sit_id = "sit-ai-infra-risk"
            if sit_id not in self.situations:
                self.situations[sit_id] = Situation(
                    situation_id=sit_id,
                    name="AI Infrastructure Capacity & Cost Risk",
                    anomalies=[a.anomaly_id for a in active_anoms if a.metric in ["cloud_cost", "gpu_demand"]],
                    risk_level="HIGH"
                )
