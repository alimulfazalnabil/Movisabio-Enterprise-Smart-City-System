from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class StrategyDriftStatus(str, enum.Enum):
    ALIGNED = "ALIGNED"
    WARNING = "WARNING"
    DRIFT_DETECTED = "DRIFT_DETECTED"

class StrategyMetric(BaseModel):
    metric_id: str
    name: str
    expected_value: float
    observed_value: float
    variance_threshold: float = 0.1 # 10% allowed variance
    last_evaluated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @property
    def variance(self) -> float:
        if self.expected_value == 0:
            return 0.0
        return abs(self.observed_value - self.expected_value) / self.expected_value
        
    @property
    def status(self) -> StrategyDriftStatus:
        if self.variance > self.variance_threshold * 2:
            return StrategyDriftStatus.DRIFT_DETECTED
        elif self.variance > self.variance_threshold:
            return StrategyDriftStatus.WARNING
        return StrategyDriftStatus.ALIGNED

class StrategyDriftEngine:
    def __init__(self):
        self.metrics: Dict[str, StrategyMetric] = {}
        
    def record_observation(self, metric_id: str, name: str, expected: float, observed: float) -> StrategyMetric:
        metric = StrategyMetric(
            metric_id=metric_id,
            name=name,
            expected_value=expected,
            observed_value=observed
        )
        self.metrics[metric_id] = metric
        return metric
        
    def check_overall_drift(self) -> bool:
        # If any metric indicates drift, return True
        for metric in self.metrics.values():
            if metric.status == StrategyDriftStatus.DRIFT_DETECTED:
                return True
        return False
