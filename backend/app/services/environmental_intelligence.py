from typing import Dict, Any, List

class EnvironmentalIntelligenceEngine:
    """
    B10 - Territorial Sustainability Intelligence Engine
    Coordinates environment, climate, and sustainability optimization.
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def estimate_traffic_emissions(self, traffic_flow: float, avg_speed: float, idle_ratio: float) -> Dict[str, float]:
        """
        B10.7 - Traffic -> Emission Intelligence
        Estimates emissions based on flow, speed, and idling.
        """
        # Simplistic proxy model
        # Base emission factor at optimal speed ~ 60 km/h
        base_ef_co2 = 120.0 # g/km per vehicle
        base_ef_nox = 0.5   # g/km per vehicle
        
        # Speed penalty: high emissions at very low speeds, and very high speeds
        speed_penalty = 1.0
        if avg_speed < 20.0:
            speed_penalty = 2.5
        elif avg_speed > 100.0:
            speed_penalty = 1.5
            
        # Idling penalty
        idling_penalty = 1.0 + (idle_ratio * 3.0)
        
        total_co2_kg = (traffic_flow * base_ef_co2 * speed_penalty * idling_penalty) / 1000.0
        total_nox_kg = (traffic_flow * base_ef_nox * speed_penalty * idling_penalty) / 1000.0
        
        return {
            "estimated_co2_kg": total_co2_kg,
            "estimated_nox_kg": total_nox_kg,
            "validation_status": "MODELED_UNVALIDATED"
        }

    def assess_flood_risk(self, rainfall_mm: float, drainage_capacity: float, terrain_factor: float) -> Dict[str, Any]:
        """
        B10.13 - Urban Flood Intelligence
        Combines rainfall and drainage constraints to model risk.
        """
        net_water = rainfall_mm * terrain_factor - drainage_capacity
        
        if net_water > 50.0:
            risk_level = "HIGH"
            time_to_impact = "1 HOUR"
        elif net_water > 10.0:
            risk_level = "MODERATE"
            time_to_impact = "4 HOURS"
        else:
            risk_level = "LOW"
            time_to_impact = "N/A"
            
        return {
            "net_water_excess_mm": net_water,
            "risk_level": risk_level,
            "time_to_impact": time_to_impact
        }

    def evaluate_pareto_sustainability(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        B10.28 - Multi-Objective Sustainability Optimization
        Evaluates interventions on a Pareto frontier (Mobility vs Emissions vs Risk).
        """
        pareto_frontier = []
        for s in scenarios:
            cost = s.get("mobility_cost", 100)
            emissions = s.get("emissions", 100)
            
            # Simple heuristic: If scenario is strictly dominated, discard.
            # In production, use standard pareto sorting (e.g. Non-dominated Sorting)
            is_dominated = False
            for other in scenarios:
                if other == s:
                    continue
                if other.get("mobility_cost", 100) <= cost and other.get("emissions", 100) <= emissions:
                    if other.get("mobility_cost", 100) < cost or other.get("emissions", 100) < emissions:
                        is_dominated = True
                        break
            
            if not is_dominated:
                s["pareto_optimal"] = True
                pareto_frontier.append(s)
                
        return pareto_frontier
