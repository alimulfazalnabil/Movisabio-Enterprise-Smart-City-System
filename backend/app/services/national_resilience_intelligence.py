from typing import Dict, Any, List

class NationalResilienceIntelligenceEngine:
    """
    B33 - National Resilience, Strategic Security & Critical Systems Intelligence
    Models essential service continuity, cascades infrastructure failures, and evaluates resource reserves.
    """

    def evaluate_service_continuity(self, current_capacity: float, minimum_viable_level: float) -> Dict[str, Any]:
        """
        B33.6 - Essential Services Model
        Checks if a critical service has dropped below its Minimum Viable Service Level (MVSL).
        """
        is_breached = current_capacity < minimum_viable_level
        status = "CRITICAL_FAILURE" if is_breached else "OPERATIONAL"
        
        return {
            "current_capacity_pct": current_capacity,
            "minimum_viable_level_pct": minimum_viable_level,
            "status": status,
            "continuity_risk": "HIGH" if (current_capacity - minimum_viable_level) < 10 else "LOW"
        }

    def simulate_infrastructure_cascade(self, failed_asset_id: str, dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        B33.9 - Cascading Failure Simulation
        Maps how a failure in one critical system (e.g., power) propagates to dependent systems.
        """
        # Mock cascade traversal
        direct_dependencies = dependency_graph.get(failed_asset_id, [])
        cascading_impacts = len(direct_dependencies)
        
        return {
            "trigger_asset": failed_asset_id,
            "systems_directly_impacted": direct_dependencies,
            "estimated_cascade_severity": "HIGH" if cascading_impacts > 2 else "MODERATE",
            "required_mitigation": "Activate backup resources for dependent systems immediately."
        }

    def evaluate_strategic_reserves(self, current_stock: float, daily_burn_rate: float, target_days: float) -> Dict[str, Any]:
        """
        B33.13 - Strategic Reserve Intelligence
        Calculates if emergency reserves are sufficient for a specific disruption scenario.
        """
        days_coverage = (current_stock / daily_burn_rate) if daily_burn_rate > 0 else float('inf')
        is_sufficient = days_coverage >= target_days
        
        return {
            "current_stock": current_stock,
            "burn_rate": daily_burn_rate,
            "estimated_days_coverage": round(days_coverage, 1),
            "target_scenario_days": target_days,
            "reserve_status": "SUFFICIENT" if is_sufficient else "DEFICIT",
            "deficit_amount": max(0, (target_days * daily_burn_rate) - current_stock)
        }
