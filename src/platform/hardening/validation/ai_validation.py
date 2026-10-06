from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class AIValidationStage(str, enum.Enum):
    DATASET = "DATASET"
    MODEL_EVAL = "MODEL_EVAL"
    ROBUSTNESS = "ROBUSTNESS"
    SIMULATION = "SIMULATION"
    HIL = "HIL"
    SHADOW = "SHADOW"
    APPROVED = "APPROVED"

class ModelValidationProfile(BaseModel):
    model_id: str
    stage: AIValidationStage = AIValidationStage.DATASET
    metrics: Dict[str, float] = Field(default_factory=dict)
    safety_invariants_checked: bool = False
    shadow_mode_duration_hrs: int = 0
    
class AIValidator:
    def __init__(self):
        self.profiles: Dict[str, ModelValidationProfile] = {}
        
    def register_model(self, model_id: str) -> ModelValidationProfile:
        profile = ModelValidationProfile(model_id=model_id)
        self.profiles[model_id] = profile
        return profile
        
    def record_metrics(self, model_id: str, precision: float, recall: float, latency_ms: float):
        if model_id not in self.profiles:
            raise ValueError("Model not found")
            
        profile = self.profiles[model_id]
        profile.metrics.update({
            "precision": precision,
            "recall": recall,
            "latency_ms": latency_ms
        })
        
    def advance_stage(self, model_id: str, stage: AIValidationStage):
        if model_id not in self.profiles:
            raise ValueError("Model not found")
            
        profile = self.profiles[model_id]
        
        if stage == AIValidationStage.APPROVED and not profile.safety_invariants_checked:
            raise ValueError("Cannot approve without safety invariants checked")
            
        if stage == AIValidationStage.APPROVED and profile.shadow_mode_duration_hrs < 24:
            raise ValueError("Cannot approve without at least 24h shadow mode")
            
        profile.stage = stage
