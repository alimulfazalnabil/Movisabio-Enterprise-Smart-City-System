from typing import List
from src.services.nature.models.schemas import BiodiversityIndicator

class BiodiversityEngine:
    def calculate_health(self, richness: float, diversity: float, connectivity: float, territory_id: str) -> BiodiversityIndicator:
        """
        Calculates a multi-dimensional biodiversity health state without reducing to a single opaque score.
        """
        # Composite evaluation
        composite = (richness + diversity + connectivity) / 3.0
        
        health = "STABLE"
        if composite < 0.4:
            health = "DEGRADED"
        elif composite > 0.7:
            health = "RESTORING"
            
        return BiodiversityIndicator(
            territory_id=territory_id,
            species_richness_score=richness,
            habitat_diversity_score=diversity,
            connectivity_score=connectivity,
            overall_health=health
        )
