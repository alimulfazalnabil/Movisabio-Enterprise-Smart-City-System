from typing import List, Dict
from src.services.energy.models.schemas import GridOutage, CriticalLoadAsset

class OutageImpactEngine:
    def assess_impact(self, outage_id: str, affected_feeders: List[str], feeder_load_map: Dict[str, List[CriticalLoadAsset]]) -> GridOutage:
        """
        Assesses the impact of an outage on critical loads based on affected feeders.
        """
        affected_critical_loads = []
        
        for feeder in affected_feeders:
            if feeder in feeder_load_map:
                for asset in feeder_load_map[feeder]:
                    affected_critical_loads.append(asset.asset_id)
                    
        return GridOutage(
            outage_id=outage_id,
            affected_feeders=affected_feeders,
            status="IMPACT_ASSESSED",
            affected_critical_loads=affected_critical_loads
        )
