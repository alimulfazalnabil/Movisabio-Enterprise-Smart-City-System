from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, Optional

class EntitySource(BaseModel):
    type: str
    id: str

class EntityEnvelope(BaseModel):
    entity_id: str
    entity_type: str
    
    tenant_id: str
    
    version: int = 1
    
    status: str
    
    valid_from: datetime
    valid_to: Optional[datetime] = None
    
    source: EntitySource
    
    data_quality: str
    
    geometry: Dict[str, Any] = Field(default_factory=dict)
