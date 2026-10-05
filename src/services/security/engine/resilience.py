from src.services.security.models.schemas import ResilienceScenario, CyberPhysicalAsset
from typing import Dict, List

class ResilienceEngine:
    def __init__(self, dependency_graph: Dict[str, List[str]]):
        # Maps an asset ID to a list of dependent asset IDs
        self.dependency_graph = dependency_graph
        
    def simulate_scenario(self, scenario: ResilienceScenario) -> List[str]:
        """
        Simulates the cascading impact of an asset failure.
        Returns a list of affected asset IDs.
        """
        affected = set()
        queue = [scenario.target_asset_id]
        
        while queue:
            current = queue.pop(0)
            if current not in affected:
                affected.add(current)
                # Add all dependencies that rely on this asset
                if current in self.dependency_graph:
                    queue.extend(self.dependency_graph[current])
                    
        return list(affected)
