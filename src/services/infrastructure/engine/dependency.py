from typing import List, Set, Dict
from src.services.infrastructure.models.schemas import AssetDependency

class DependencyGraphEngine:
    """
    Evaluates failure impact across the infrastructure network.
    """
    
    def __init__(self, dependencies: List[AssetDependency]):
        self.edges = dependencies
        self.adj_list: Dict[str, List[AssetDependency]] = {}
        for edge in self.edges:
            if edge.source_asset_id not in self.adj_list:
                self.adj_list[edge.source_asset_id] = []
            self.adj_list[edge.source_asset_id].append(edge)
            
    def get_downstream_impact(self, failed_asset_id: str) -> List[str]:
        """
        Returns a list of all asset IDs that are affected by a failure at the failed_asset_id.
        """
        impacted: Set[str] = set()
        queue = [failed_asset_id]
        
        while queue:
            current = queue.pop(0)
            if current in self.adj_list:
                for edge in self.adj_list[current]:
                    if edge.target_asset_id not in impacted:
                        impacted.add(edge.target_asset_id)
                        queue.append(edge.target_asset_id)
                        
        return list(impacted)
