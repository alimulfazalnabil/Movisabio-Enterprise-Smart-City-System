from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TrafficPrediction(BaseModel):
    """
    Standardized traffic forecast metric output providing the exact expectation 
    over a future horizon, including confidence bounds.
    """
    prediction_id: str
    tenant_id: str
    
    intersection_id: str
    approach_id: Optional[str] = None
    
    generated_at: datetime
    target_time: datetime
    horizon_seconds: int
    
    metric: str  # e.g., 'queue_length', 'congestion_index'
    predicted_value: float
    
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    confidence: float
    
    model_id: str
    model_version: str
    feature_version: str
    data_quality: float
