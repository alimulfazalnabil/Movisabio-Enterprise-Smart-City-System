from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class ModelStatus(str, enum.Enum):
    ONLINE = "ONLINE"
    SHADOW = "SHADOW"
    CANARY = "CANARY"
    DEGRADED = "DEGRADED"
    ROLLBACK = "ROLLBACK"

class AIModelHealth(BaseModel):
    model_id: str
    version: str
    tenant_id: str
    status: ModelStatus = ModelStatus.ONLINE
    drift_score: float = 0.0
    accuracy: float = 1.0
    last_evaluated: datetime = Field(default_factory=datetime.utcnow)

class AIOpsEngine:
    def __init__(self):
        self.models: Dict[str, AIModelHealth] = {}
        
    def deploy_model(self, model: AIModelHealth) -> AIModelHealth:
        self.models[model.model_id] = model
        return model
        
    def evaluate_drift(self, model_id: str, drift_score: float, current_accuracy: float) -> AIModelHealth:
        if model_id not in self.models:
            raise ValueError("Model not found")
            
        model = self.models[model_id]
        model.drift_score = drift_score
        model.accuracy = current_accuracy
        model.last_evaluated = datetime.utcnow()
        
        if drift_score > 0.3 or current_accuracy < 0.8:
            model.status = ModelStatus.DEGRADED
            
        return model
