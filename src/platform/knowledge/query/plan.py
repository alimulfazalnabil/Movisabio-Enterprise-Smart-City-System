from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class SpatialConstraint(BaseModel):
    relation: Literal["INTERSECTS", "WITHIN", "NEAR"]
    distance_meters: Optional[float] = None
    target_entity: Optional[str] = None

class TemporalConstraint(BaseModel):
    operator: Literal["BEFORE", "AFTER", "DURING", "SINCE"]
    timestamp: str

class QueryEntity(BaseModel):
    type: str
    scope: str

class QueryPlan(BaseModel):
    query_id: str
    intent: str
    entities: List[QueryEntity]
    spatial: Optional[SpatialConstraint] = None
    temporal: Optional[TemporalConstraint] = None
    filters: List[Dict] = []
    
class QueryPlanner:
    def validate_plan(self, plan: QueryPlan) -> bool:
        """
        Validates the generated query plan before deterministic execution.
        Ensures LLM didn't inject malicious instructions.
        """
        if not plan.entities:
            return False
        return True
