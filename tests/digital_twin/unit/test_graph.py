import pytest
from src.services.digital_twin.models.schemas import TwinRelationship
from src.services.digital_twin.engine.graph import TerritorialGraphEngine

def test_graph_downstream_impacts():
    engine = TerritorialGraphEngine()
    
    engine.add_relationship(TwinRelationship(relationship_id="1", source_entity_id="FLOOD_ZONE", target_entity_id="ROAD-1", relationship_type="AFFECTS"))
    engine.add_relationship(TwinRelationship(relationship_id="2", source_entity_id="ROAD-1", target_entity_id="INT-1", relationship_type="CONNECTED_TO"))
    engine.add_relationship(TwinRelationship(relationship_id="3", source_entity_id="INT-1", target_entity_id="HOSPITAL-1", relationship_type="SUPPLIES"))
    
    impacted = engine.get_downstream_impacts("FLOOD_ZONE", max_depth=3)
    
    assert "ROAD-1" in impacted
    assert "INT-1" in impacted
    assert "HOSPITAL-1" in impacted
    assert len(impacted) == 3

def test_graph_circular_dependency():
    engine = TerritorialGraphEngine()
    
    engine.add_relationship(TwinRelationship(relationship_id="1", source_entity_id="NODE-A", target_entity_id="NODE-B", relationship_type="CONNECTED_TO"))
    engine.add_relationship(TwinRelationship(relationship_id="2", source_entity_id="NODE-B", target_entity_id="NODE-A", relationship_type="CONNECTED_TO"))
    
    impacted = engine.get_downstream_impacts("NODE-A", max_depth=5)
    
    # Should not infinite loop, length is 1 (B) + itself if we counted it, but we only add targets, so B and A.
    assert "NODE-B" in impacted
    assert "NODE-A" in impacted
    assert len(impacted) == 2
