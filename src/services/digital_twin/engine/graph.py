from typing import List
from src.services.digital_twin.models.schemas import TwinRelationship

class TerritorialGraphEngine:
    """
    Manages and queries the territorial knowledge graph.
    """
    
    def __init__(self):
        self.relationships: List[TwinRelationship] = []
        
    def add_relationship(self, rel: TwinRelationship):
        self.relationships.append(rel)
        
    def get_downstream_impacts(self, source_entity_id: str, max_depth: int = 3) -> List[str]:
        """
        Traverses relationships like 'AFFECTS', 'SUPPLIES', 'SERVED_BY' to find downstream entities.
        """
        impacted = set()
        queue = [(source_entity_id, 0)]
        visited = set()
        
        while queue:
            current_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue
                
            if current_id in visited:
                continue
            visited.add(current_id)
            
            for rel in self.relationships:
                if rel.source_entity_id == current_id and rel.relationship_type in ["AFFECTS", "SUPPLIES", "CONNECTED_TO"]:
                    impacted.add(rel.target_entity_id)
                    queue.append((rel.target_entity_id, depth + 1))
                    
        return list(impacted)
