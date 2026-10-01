from typing import Dict, Any
from src.services.climate.models.schemas import ClimateScenario

class ScenarioSimulationEngine:
    """
    Executes what-if climate and sustainability scenarios against baseline data.
    """
    
    def simulate_ev_adoption_impact(self, scenario: ClimateScenario, baseline_emissions_kg: float) -> Dict[str, Any]:
        """
        Simulates the carbon impact of a fleet electrification intervention.
        """
        ev_adoption_target = 0.0
        
        # Extract intervention parameter
        for intervention in scenario.interventions:
            if intervention.get("type") == "EV_ADOPTION":
                ev_adoption_target = float(intervention.get("target_percentage", 0.0))
                
        if ev_adoption_target > 100 or ev_adoption_target < 0:
            raise ValueError("Target percentage must be between 0 and 100")
            
        # Simplified simulation: reduce emissions proportionally to EV adoption
        # (Assuming grid carbon intensity is zero for simplicity in this mock)
        reduction_factor = ev_adoption_target / 100.0
        reduced_emissions = baseline_emissions_kg * (1.0 - reduction_factor)
        
        return {
            "scenario_id": scenario.scenario_id,
            "baseline_emissions_kg": baseline_emissions_kg,
            "scenario_emissions_kg": reduced_emissions,
            "avoided_emissions_kg": baseline_emissions_kg - reduced_emissions,
            "assumptions_used": ["Zero-carbon grid", "1:1 ICE to EV replacement"]
        }
