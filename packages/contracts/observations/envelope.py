from pydantic import BaseModel
from datetime import datetime
from typing import Any

class ObservationSource(BaseModel):
    device_id: str

class ObservationEnvelope(BaseModel):
    observation_id: str
    subject_id: str
    observation_type: str
    
    observed_at: datetime
    
    value: Any
    unit: str
    
    source: ObservationSource
    
    quality: str
    confidence: float
