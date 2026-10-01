from typing import Dict, Any
from src.services.territory.models.schemas import DevelopmentScenario

class DevelopmentScenarioEngine:
    """
    Evaluates infrastructure capacity against a proposed development scenario.
    """
    
    def evaluate_capacity(self, scenario: DevelopmentScenario, existing_capacity: Dict[str, float]) -> Dict[str, Any]:
        """
        existing_capacity: dict with keys like 'water_lpd', 'energy_kwh', 'traffic_trips'
        Returns impact assessment.
        """
        water_impact = scenario.estimated_water_demand_lpd / existing_capacity.get("water_lpd", 1)
        energy_impact = scenario.estimated_energy_demand_kwh / existing_capacity.get("energy_kwh", 1)
        traffic_impact = scenario.estimated_trip_generation / existing_capacity.get("traffic_trips", 1)
        
        return {
            "water_impact_ratio": water_impact,
            "energy_impact_ratio": energy_impact,
            "traffic_impact_ratio": traffic_impact,
            "viable": water_impact < 0.9 and energy_impact < 0.9 and traffic_impact < 0.9,
            "warnings": [
                "Water capacity approaching limit" if water_impact > 0.8 else None,
                "Traffic capacity approaching limit" if traffic_impact > 0.8 else None
            ]
        }
