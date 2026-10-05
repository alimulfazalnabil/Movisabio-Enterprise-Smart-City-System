from abc import ABC, abstractmethod
from typing import List, Optional
from src.services.knowledge_graph.domain.entities import TerritorialEntity, TerritorialRelationship, KnowledgeClaim

class GraphRepository(ABC):
    @abstractmethod
    def create_entity(self, entity: TerritorialEntity) -> None:
        pass
        
    @abstractmethod
    def create_relationship(self, relationship: TerritorialRelationship) -> None:
        pass
        
    @abstractmethod
    def get_entity(self, entity_id: str) -> Optional[TerritorialEntity]:
        pass
        
    @abstractmethod
    def get_outgoing_relationships(self, entity_id: str, rel_type: Optional[str] = None) -> List[TerritorialRelationship]:
        pass
        
    @abstractmethod
    def get_incoming_relationships(self, entity_id: str, rel_type: Optional[str] = None) -> List[TerritorialRelationship]:
        pass
