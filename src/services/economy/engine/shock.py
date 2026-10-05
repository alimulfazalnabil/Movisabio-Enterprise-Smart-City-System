from src.services.economy.models.schemas import EconomicShockEvent, EconomicResilience

class EconomicShockEngine:
    def evaluate_impact(self, event: EconomicShockEvent, resilience: EconomicResilience) -> str:
        """
        Evaluates the economic impact of a shock event on a zone based on its resilience score.
        """
        impact_multiplier = {
            "LOW": 1.0,
            "MODERATE": 2.0,
            "HIGH": 3.0,
            "CRITICAL": 5.0
        }
        
        base_impact = impact_multiplier.get(event.severity, 1.0)
        
        # Higher resilience reduces impact
        adjusted_impact = base_impact / max(resilience.resilience_index, 0.1)
        
        if adjusted_impact >= 4.0:
            return "SEVERE_DISRUPTION"
        elif adjusted_impact >= 2.0:
            return "MODERATE_DISRUPTION"
        return "MANAGEABLE"
