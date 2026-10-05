from src.services.knowledge_graph.domain.entities import TerritorialEntity, TerritorialRelationship
from src.services.knowledge_graph.repository.implementations import InMemoryGraphRepository
from src.services.knowledge_graph.query.semantic_query import SemanticEngine
import uuid

def test_semantic_dependency_traversal():
    repo = InMemoryGraphRepository()
    engine = SemanticEngine(repo)
    
    # Substation B
    substation = TerritorialEntity(
        entity_id="SUB-1",
        tenant_id="T1",
        entity_type="SUBSTATION",
        status="ACTIVE",
        criticality="C2",
        data_classification="RESTRICTED"
    )
    repo.create_entity(substation)
    
    # Water Pump
    water_pump = TerritorialEntity(
        entity_id="PUMP-1",
        tenant_id="T1",
        entity_type="WATER_FACILITY",
        status="ACTIVE",
        criticality="C3",
        data_classification="RESTRICTED"
    )
    repo.create_entity(water_pump)
    
    # Hospital
    hospital = TerritorialEntity(
        entity_id="HOSP-1",
        tenant_id="T1",
        entity_type="HOSPITAL",
        status="ACTIVE",
        criticality="C4",
        data_classification="CONFIDENTIAL"
    )
    repo.create_entity(hospital)
    
    # Relationships
    # Water Pump depends on Substation
    rel1 = TerritorialRelationship(
        relationship_id=str(uuid.uuid4()),
        source_entity_id="PUMP-1",
        relationship_type="DEPENDS_ON",
        target_entity_id="SUB-1",
        confidence=1.0,
        verification_status="VERIFIED"
    )
    repo.create_relationship(rel1)
    
    # Hospital depends on Water Pump
    rel2 = TerritorialRelationship(
        relationship_id=str(uuid.uuid4()),
        source_entity_id="HOSP-1",
        relationship_type="DEPENDS_ON",
        target_entity_id="PUMP-1",
        confidence=1.0,
        verification_status="VERIFIED"
    )
    repo.create_relationship(rel2)
    
    # Query: What critical things depend on Substation?
    results = engine.find_dependent_critical_infrastructure("SUB-1")
    
    assert len(results) == 2
    
    entity_ids = [r["entity"].entity_id for r in results]
    assert "PUMP-1" in entity_ids
    assert "HOSP-1" in entity_ids
    
    # Check paths
    hosp_res = next(r for r in results if r["entity"].entity_id == "HOSP-1")
    assert hosp_res["path"] == ["SUB-1", "PUMP-1", "HOSP-1"]
