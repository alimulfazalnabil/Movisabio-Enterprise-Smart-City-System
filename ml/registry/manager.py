from pydantic import BaseModel
import datetime
from typing import Optional

class MLModelRegistry(BaseModel):
    model_id: str
    version: str
    architecture: str # e.g. "LSTM", "YOLOv10", "BoT-SORT"
    deployment_status: str # "SHADOW", "CANDIDATE", "PRODUCTION", "DEPRECATED"
    training_date: datetime.datetime
    metrics: dict
    weights_uri: str
    
class ModelManager:
    """
    Phase 10: Model Registry
    Every model needs model ID, version, deployment status, and metrics.
    """
    def __init__(self):
        self.registry = {}
        
    def register_model(self, model: MLModelRegistry):
        self.registry[f"{model.model_id}:{model.version}"] = model
        
    def get_production_model(self, architecture: str) -> Optional[MLModelRegistry]:
        for model in self.registry.values():
            if model.architecture == architecture and model.deployment_status == "PRODUCTION":
                return model
        return None
