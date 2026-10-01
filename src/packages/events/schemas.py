from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum
import uuid
from datetime import datetime

class DataQuality(str, Enum):
    VALID = "VALID"
    SUSPECT = "SUSPECT"
    STALE = "STALE"
    INVALID = "INVALID"
    MISSING = "MISSING"

class SourceRef(BaseModel):
    type: str  # camera, sensor, gps, weather_api
    id: str

class LocationRef(BaseModel):
    latitude: float
    longitude: float

class CanonicalEvent(BaseModel):
    """
    The normalized base event schema for all MoviSabio ingestion.
    """
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex}")
    event_type: str
    event_version: str = "1.0"
    
    tenant_id: str
    site_id: Optional[str] = None
    intersection_id: Optional[str] = None
    
    source: SourceRef
    
    # Timing architecture for accurate latency measurement
    event_time: datetime         # Time the event occurred in the physical world
    ingestion_time: datetime     # Time the ingestion gateway received it
    processing_time: Optional[datetime] = None  # Time it finished being processed
    
    location: Optional[LocationRef] = None
    
    data_quality: DataQuality = DataQuality.VALID
    
    payload: Dict[str, Any]
