from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel

class TrafficFeatureVector(BaseModel):
    """
    Canonical feature representation for the ML prediction engine.
    Detaches prediction logic from raw operational database schemas.
    """
    timestamp: datetime
    intersection_id: str
    approach_id: Optional[str] = None
    lane_id: Optional[str] = None
    
    # Core numeric features
    volume: float
    speed: float
    density: float
    queue_length: float
    occupancy: float
    delay: float
    congestion_index: float
    
    # Operational features
    signal_phase: str
    phase_elapsed: float
    incident_indicator: float
    
    # External features
    weather_features: Dict[str, float]
    
    # Validation gates
    data_quality: float
