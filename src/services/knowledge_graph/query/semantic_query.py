from typing import List, Dict, Any
from src.services.knowledge_graph.repository.interface import GraphRepository

class SemanticEngine:
    def __init__(self, repo: GraphRepository):
        self.repo = repo
        
    def find_dependent_critical_infrastructure(self, target_entity_id: str) -> List[Dict[str, Any]]:
        """
        Example semantic query:
        Find all critical infrastructure (C3, C4) that depends (directly or indirectly) on this target_entity.
        This answers: "If this substation fails, what critical assets are affected?"
        """
        results = []
        visited = set()
        
        def traverse(entity_id: str, path: List[str]):
            if entity_id in visited:
                return
            visited.add(entity_id)
            
            # Find incoming dependencies
            incoming = self.repo.get_incoming_relationships(entity_id, rel_type="DEPENDS_ON")
            for rel in incoming:
                source_ent = self.repo.get_entity(rel.source_entity_id)
                if source_ent:
                    new_path = path + [source_ent.entity_id]
                    if source_ent.criticality in ["C3", "C4"]:
                        results.append({
                            "entity": source_ent,
                            "path": new_path
                        })
                    # Recurse
                    traverse(source_ent.entity_id, new_path)
                    
        traverse(target_entity_id, [target_entity_id])
        return results
