from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class TwinEntity(BaseModel):
    twin_entity_id: str
    tenant_id: str
    territory_id: str
    entity_type: str
    entity_subtype: str
    geometry: Optional[dict] = None
    parent_entity_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TwinRelationship(BaseModel):
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str # LOCATED_IN, CONNECTED_TO, SERVED_BY, AFFECTS

class TwinState(BaseModel):
    state_id: str
    twin_entity_id: str
    state_data: Dict[str, Any]
    confidence: float
    source: str
    model_version: Optional[str] = None
    observed_at: datetime
    processed_at: datetime
    data_quality: str

class SimulationJob(BaseModel):
    job_id: str
    scenario_id: str
    baseline_twin_version: str
    simulation_engine: str # SUMO, FLOOD, ENERGY
    engine_version: str
    parameters: Dict[str, Any]
    status: str # QUEUED, RUNNING, COMPLETED, FAILED
    result_data: Optional[Dict[str, Any]] = None
    created_at: datetime

class CounterfactualEvaluation(BaseModel):
    evaluation_id: str
    intervention_id: str
    baseline_scenario_id: str
    actual_scenario_id: str
    metrics_compared: List[str]
    estimated_effects: Dict[str, float]
    uncertainty: Dict[str, float]
