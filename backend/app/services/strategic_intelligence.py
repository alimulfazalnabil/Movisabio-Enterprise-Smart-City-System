from typing import Dict, Any, List

class StrategicIntelligenceEngine:
    """
    B32 - Geopolitical, Strategic & Global Risk Intelligence
    Calculates strategic dependencies, cascades risk events, and evaluates resilience.
    """

    def calculate_dependency_exposure(self, import_volume: float, total_demand: float, supplier_concentration: float) -> Dict[str, Any]:
        """
        B32.4 - Strategic Dependency Index
        Calculates the vulnerability of a territory to supply chain shocks.
        """
        dependency_ratio = (import_volume / total_demand) if total_demand > 0 else 0
        exposure_score = dependency_ratio * supplier_concentration
        
        status = "HIGH_VULNERABILITY" if exposure_score > 0.6 else "RESILIENT"
        
        return {
            "dependency_ratio": round(dependency_ratio, 2),
            "supplier_concentration": round(supplier_concentration, 2),
            "exposure_score": round(exposure_score, 2),
            "strategic_status": status
        }

    def simulate_cascading_risk(self, trigger_event: str, primary_impact_value: float) -> Dict[str, Any]:
        """
        B32.15 - Cascading Risk Engine
        Propagates a geopolitical or macro shock through the economic and physical layers.
        """
        # Simplified propagation logic
        secondary_impact = primary_impact_value * 1.5 # e.g. industrial slowdown
        tertiary_impact = secondary_impact * 0.8      # e.g. local employment impact
        
        return {
            "trigger": trigger_event,
            "direct_infrastructure_impact": primary_impact_value,
            "cascading_economic_impact": secondary_impact,
            "cascading_social_impact": tertiary_impact,
            "total_systemic_stress": primary_impact_value + secondary_impact + tertiary_impact
        }

    def evaluate_resilience_options(self, current_exposure: float, diversification_cost: float, stockpile_cost: float) -> List[Dict[str, Any]]:
        """
        B32.16 - Strategic Resilience Modeling
        Compares strategic options to mitigate geopolitical dependencies.
        """
        options = []
        
        if current_exposure > 0.5:
            options.append({
                "strategy": "Supplier Diversification",
                "estimated_cost": diversification_cost,
                "exposure_reduction": "-40%",
                "time_to_implement": "2-3 Years"
            })
            options.append({
                "strategy": "Strategic Stockpiling",
                "estimated_cost": stockpile_cost,
                "exposure_reduction": "Provides 90-day buffer",
                "time_to_implement": "6 Months"
            })
            
        return options
