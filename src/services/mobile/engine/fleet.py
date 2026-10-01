from typing import List, Optional
from src.services.mobile.models.schemas import MobileAsset, MissionPackage

class FleetOptimizationEngine:
    """
    Assigns assets to missions based on distance, battery, and capability.
    """
    
    def assign_mission(self, mission: MissionPackage, available_assets: List[MobileAsset]) -> Optional[str]:
        """
        Returns the asset_id of the best asset for the mission, or None if no suitable asset exists.
        """
        best_asset = None
        highest_score = -1
        
        for asset in available_assets:
            if asset.status != "AVAILABLE":
                continue
                
            if asset.battery_state < 30.0: # Minimum battery safety margin
                continue
                
            # Mock scoring: favor higher battery
            score = asset.battery_state
            
            if score > highest_score:
                highest_score = score
                best_asset = asset
                
        return best_asset.asset_id if best_asset else None
