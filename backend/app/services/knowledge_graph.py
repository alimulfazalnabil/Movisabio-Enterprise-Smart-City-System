from typing import Dict, Any, List

class KnowledgeGraphBuilder:
    """
    B8.25 - Network Knowledge Graph
    Translates the relational database into a semantic graph for Territorial Intelligence.
    """
    def __init__(self):
        self.nodes = []
        self.edges = []

    def build_from_corridor(self, corridor: Dict[str, Any], intersections: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Add Corridor Node
        self.nodes.append({"id": corridor["corridor_id"], "type": "Corridor", "properties": corridor})
        
        for idx in intersections:
            idx_id = idx["intersection_id"]
            self.nodes.append({"id": idx_id, "type": "Intersection", "properties": idx})
            # Corridor -> Intersection
            self.edges.append({"source": corridor["corridor_id"], "target": idx_id, "relation": "CONTAINS"})
            
        for rel in relationships:
            # Semantic mapping
            relation_type = rel["relationship_type"]
            if relation_type == "UPSTREAM":
                sem_rel = "UPSTREAM_OF"
            elif relation_type == "DOWNSTREAM":
                sem_rel = "DOWNSTREAM_OF"
            else:
                sem_rel = "CONNECTS_TO"
                
            self.edges.append({
                "source": rel["source_id"],
                "target": rel["target_id"],
                "relation": sem_rel,
                "properties": {"distance": rel.get("distance_m")}
            })
            
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
