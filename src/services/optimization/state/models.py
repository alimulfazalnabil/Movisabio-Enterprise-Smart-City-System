from datetime import datetime
from typing import List
from pydantic import BaseModel

class OptimizationState(BaseModel):
    """
    Normalized feature state specifically formatted for RL/Optimization model input.
    """
    timestamp: datetime
    intersection_id: str
    
    # Normalized 0.0-1.0 features
    lane_features: List[float]
    approach_features: List[float]
    queue_lengths: List[float]
    speeds: List[float]
    densities: List[float]
    flows: List[float]
    
    congestion_index: float
    
    # Controller context
    signal_phase: str
    phase_elapsed: float
    remaining_green: float
    
    # Future awareness
    predicted_queue: List[float]
    predicted_speed: List[float]
    
    incident_flags: List[float]
    data_quality: float
    
    state_schema_version: str = "1.0"
