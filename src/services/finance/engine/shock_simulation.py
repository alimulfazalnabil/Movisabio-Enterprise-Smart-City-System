from src.services.finance.models.schemas import EconomicShock, ShockImpact
from typing import Dict, List

class EconomicShockEngine:
    def __init__(self, dependency_graph: Dict[str, List[str]]):
        """
        dependency_graph maps a shock type to the sectors it immediately impacts.
        """
        self.dependency_graph = dependency_graph
        
    def simulate_shock(self, shock: EconomicShock) -> ShockImpact:
        """
        Simulates the economic impact of a shock propagating through dependent sectors.
        """
        affected_sectors = self.dependency_graph.get(shock.shock_type, [])
        
        # Simple simulated impact calculation: Base sector cost * shock magnitude
        # We will use a mock multiplier for demonstration purposes.
        base_multiplier = 1000000.0
        estimated_impact = len(affected_sectors) * shock.magnitude * base_multiplier
        
        return ShockImpact(
            shock_id=shock.shock_id,
            affected_sectors=affected_sectors,
            estimated_economic_impact=estimated_impact
        )
