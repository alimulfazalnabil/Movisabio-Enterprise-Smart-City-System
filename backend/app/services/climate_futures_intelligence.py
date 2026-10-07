from typing import Dict, Any, List

class ClimateFuturesIntelligenceEngine:
    """
    B34 - Climate Adaptation, Environmental Futures & Long-Term Territorial Intelligence
    Models climate scenarios, exposure, and adaptation portfolios.
    """

    def calculate_climate_exposure(self, hazard_severity: float, asset_vulnerability: float, adaptive_capacity: float) -> Dict[str, Any]:
        """
        B34.5 - Climate Exposure Model
        Calculates localized climate risk, accounting for adaptive capacity.
        """
        raw_exposure = hazard_severity * asset_vulnerability
        residual_risk = max(0, raw_exposure - adaptive_capacity)
        
        return {
            "hazard_severity": hazard_severity,
            "asset_vulnerability": asset_vulnerability,
            "adaptive_capacity": adaptive_capacity,
            "residual_climate_risk": residual_risk,
            "status": "AT_RISK" if residual_risk > 0.5 else "ADAPTED"
        }

    def propagate_climate_impact(self, trigger_hazard: str) -> Dict[str, Any]:
        """
        B34.7 - Climate Impact Propagation
        Models how slow-onset climate hazards cascade through territorial systems.
        """
        return {
            "trigger": trigger_hazard,
            "primary_impact": "Physical Infrastructure Stress",
            "secondary_impact": "Economic Productivity Loss",
            "tertiary_impact": "Public Health Burden & Migration Pressure",
            "required_intervention": "Systemic Adaptation Planning"
        }

    def optimize_adaptation_portfolio(self, available_budget: float, candidate_interventions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B34.10 - Adaptation Optimization
        Selects the best combination of gray and green infrastructure to maximize risk reduction under a budget.
        """
        # Mock greedy selection
        selected = []
        total_cost = 0
        total_risk_reduction = 0
        
        # Sort by ROI (risk reduction per dollar)
        candidates = sorted(candidate_interventions, key=lambda x: x["risk_reduction"] / x["cost"], reverse=True)
        
        for candidate in candidates:
            if total_cost + candidate["cost"] <= available_budget:
                selected.append(candidate)
                total_cost += candidate["cost"]
                total_risk_reduction += candidate["risk_reduction"]
                
        return {
            "budget_utilized": total_cost,
            "remaining_budget": available_budget - total_cost,
            "selected_interventions": [c["name"] for c in selected],
            "total_risk_reduction_achieved": total_risk_reduction
        }
