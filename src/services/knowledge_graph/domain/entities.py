from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel

class TerritorialEntity(BaseModel):
    entity_id: str
    tenant_id: str
    entity_type: str # HOSPITAL, ROAD, SUBSTATION, FLOOD_ZONE
    name: Optional[str] = None
    status: str
    criticality: Optional[str] = None
    data_classification: str
    valid_from: Optional[datetime] = None
    properties: Dict[str, Any] = {}

class TerritorialRelationship(BaseModel):
    relationship_id: str
    source_entity_id: str
    relationship_type: str # DEPENDS_ON, LOCATED_IN, CONNECTED_BY
    target_entity_id: str
    confidence: float
    verification_status: str
    valid_from: Optional[datetime] = None

class KnowledgeClaim(BaseModel):
    claim_id: str
    subject_entity_id: str
    predicate: str
    object_entity_id: Optional[str] = None
    literal_value: Optional[Any] = None
    claim_type: str # FACT, OBSERVATION, INFERENCE, PREDICTION
    confidence: float
    provenance_source: str
