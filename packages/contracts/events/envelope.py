from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class EventSource(BaseModel):
    service: str
    instance: str

class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    event_version: str = "1.0"
    occurred_at: datetime
    published_at: datetime
    
    tenant_id: str
    organization_id: str
    
    source: EventSource
    
    correlation_id: str
    causation_id: Optional[str] = None
    
    data_classification: str = "RESTRICTED"
    
    payload: Dict[str, Any] = Field(default_factory=dict)
