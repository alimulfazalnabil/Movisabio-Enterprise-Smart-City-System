from typing import List, Optional, Dict
from src.services.knowledge_graph.domain.entities import TerritorialEntity, TerritorialRelationship
from src.services.knowledge_graph.repository.interface import GraphRepository

class InMemoryGraphRepository(GraphRepository):
    def __init__(self):
        self.entities: Dict[str, TerritorialEntity] = {}
        self.relationships: List[TerritorialRelationship] = []
        
    def create_entity(self, entity: TerritorialEntity) -> None:
        self.entities[entity.entity_id] = entity
        
    def create_relationship(self, relationship: TerritorialRelationship) -> None:
        self.relationships.append(relationship)
        
    def get_entity(self, entity_id: str) -> Optional[TerritorialEntity]:
        return self.entities.get(entity_id)
        
    def get_outgoing_relationships(self, entity_id: str, rel_type: Optional[str] = None) -> List[TerritorialRelationship]:
        return [
            r for r in self.relationships 
            if r.source_entity_id == entity_id and (rel_type is None or r.relationship_type == rel_type)
        ]
        
    def get_incoming_relationships(self, entity_id: str, rel_type: Optional[str] = None) -> List[TerritorialRelationship]:
        return [
            r for r in self.relationships 
            if r.target_entity_id == entity_id and (rel_type is None or r.relationship_type == rel_type)
        ]
