import uuid
from typing import List, Dict
from src.services.climate.models.schemas import ClimateHazard, ExposureModel

class ClimateRiskEngine:
    """
    Evaluates exposure of territorial assets to physical climate hazards.
    """
    
    def calculate_exposure(self, hazard: ClimateHazard, assets: List[Dict]) -> ExposureModel:
        """
        Calculates exposure by intersecting hazard geometry with asset geometries.
        Uses a mock spatial intersection for demonstration.
        """
        exposed = []
        
        for asset in assets:
            # Mock spatial intersection: assume assets in same mock "zone" are exposed
            if asset.get("zone") == hazard.geometry.get("zone"):
                exposed.append(asset["asset_id"])
                
        # Simple vulnerability scoring: proportion of assets exposed
        vuln_score = len(exposed) / len(assets) if assets else 0.0
        
        impact_category = "LOW"
        if vuln_score > 0.5:
            impact_category = "HIGH"
        elif vuln_score > 0.2:
            impact_category = "MEDIUM"
            
        return ExposureModel(
            exposure_id=str(uuid.uuid4()),
            hazard_id=hazard.hazard_id,
            exposed_asset_ids=exposed,
            vulnerability_score=vuln_score,
            potential_impact_category=impact_category
        )
