from typing import Dict, Any, List

class GovernmentIntelligenceEngine:
    """
    B30 - Government Administration, Public Administration & Institutional Intelligence
    Simulates administrative bottlenecks, evaluates government capacity scenarios, and tracks SLAs.
    """

    def analyze_service_bottlenecks(self, service_funnel: Dict[str, int]) -> Dict[str, Any]:
        """
        B30.5 - Administrative Workflow Intelligence
        Identifies where citizens drop out or get stuck in public service workflows.
        """
        # Mock logic
        stages = list(service_funnel.keys())
        values = list(service_funnel.values())
        max_dropoff = 0
        bottleneck_stage = "None"
        
        for i in range(1, len(values)):
            dropoff = values[i-1] - values[i]
            if dropoff > max_dropoff:
                max_dropoff = dropoff
                bottleneck_stage = stages[i]
                
        return {
            "funnel_analyzed": stages,
            "identified_bottleneck": bottleneck_stage,
            "lost_applications": max_dropoff,
            "recommendation": f"Audit procedural requirements at stage '{bottleneck_stage}'."
        }

    def simulate_government_capacity(self, demand_surge_pct: float, current_workforce: int) -> Dict[str, Any]:
        """
        B30.19 - Government Scenario Engine
        Tests the impact of sudden demand surges on institutional capacity.
        """
        required_workforce = int(current_workforce * (1 + (demand_surge_pct / 100)))
        deficit = required_workforce - current_workforce
        
        return {
            "scenario_demand_surge": f"+{demand_surge_pct}%",
            "current_capacity": current_workforce,
            "required_capacity": required_workforce,
            "capacity_deficit": deficit,
            "service_degradation_risk": "HIGH" if deficit > (current_workforce * 0.1) else "LOW"
        }

    def evaluate_program_outcomes(self, program_budget: float, measured_outcomes: Dict[str, float]) -> Dict[str, Any]:
        """
        B30.9 - Program & Policy Execution Intelligence
        Evaluates whether a government program is effectively converting budget into territorial outcomes.
        """
        # Simplified outcome assessment
        primary_metric = list(measured_outcomes.values())[0] if measured_outcomes else 0
        cost_per_outcome_unit = program_budget / primary_metric if primary_metric > 0 else 0
        
        return {
            "budget_spent": program_budget,
            "primary_outcome_achieved": primary_metric,
            "cost_per_unit": cost_per_outcome_unit,
            "execution_efficiency": "OPTIMAL" if cost_per_outcome_unit < 1500 else "NEEDS_REVIEW"
        }
