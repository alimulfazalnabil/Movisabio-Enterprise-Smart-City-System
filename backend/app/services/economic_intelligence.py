from typing import Dict, Any, List

class EconomicIntelligenceEngine:
    """
    B14 - Territorial Economic, Commerce, Tourism & Investment Intelligence
    Evaluates business locations, tourism flows, and investment suitability.
    """

    def calculate_location_score(self, candidate: Dict[str, Any], territory_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        B14.4 - Location Intelligence Engine
        Scores a candidate business location based on mobility, demographics, and infrastructure.
        """
        # Base weights for a generic retail business
        demand = territory_data.get("population_density", 0.5) * 0.20
        accessibility = territory_data.get("transit_score", 0.5) * 0.15
        competition = (1.0 - territory_data.get("competitor_density", 0.5)) * 0.15
        footfall = territory_data.get("pedestrian_flow", 0.5) * 0.15
        infrastructure = territory_data.get("utility_reliability", 0.5) * 0.10
        workforce = territory_data.get("labor_availability", 0.5) * 0.10
        tourism = territory_data.get("tourism_index", 0.5) * 0.10
        risk = (1.0 - territory_data.get("environmental_risk", 0.0)) * 0.05
        
        total_score = (demand + accessibility + competition + footfall + infrastructure + workforce + tourism + risk) * 100
        
        return {
            "location_score": round(total_score, 1),
            "breakdown": {
                "demand": demand,
                "accessibility": accessibility,
                "competition_advantage": competition,
                "footfall": footfall
            }
        }

    def analyze_job_accessibility(self, residential_zone: Dict[str, Any], employment_centers: List[Dict[str, Any]], mobility_network: Dict[str, Any]) -> Dict[str, Any]:
        """
        B14.9 - Job Accessibility Intelligence
        Calculates how many jobs are accessible within 15/30/60 minute transit windows.
        """
        # Mock calculation: assume distance / speed determines time
        accessible_15 = 0
        accessible_30 = 0
        accessible_60 = 0
        
        for center in employment_centers:
            # Mock travel time in minutes
            travel_time = center.get("distance_km", 10) / mobility_network.get("avg_speed_kmh", 20) * 60
            jobs = center.get("job_count", 0)
            
            if travel_time <= 15:
                accessible_15 += jobs
            if travel_time <= 30:
                accessible_30 += jobs
            if travel_time <= 60:
                accessible_60 += jobs
                
        return {
            "jobs_within_15m": accessible_15,
            "jobs_within_30m": accessible_30,
            "jobs_within_60m": accessible_60,
            "equity_flag": "LOW_ACCESS" if accessible_30 < 5000 else "ADEQUATE"
        }

    def simulate_tourism_shock(self, scenario: Dict[str, Any], baseline_infrastructure: Dict[str, Any]) -> Dict[str, Any]:
        """
        B14.7 - Tourism Scenario Simulation
        Simulates the impact of a major tourism surge on territorial infrastructure.
        """
        surge_pct = scenario.get("tourist_surge_pct", 0.20)
        
        # Calculate cascading pressure
        new_traffic_pressure = baseline_infrastructure.get("traffic_volume", 100) * (1 + surge_pct * 1.5)
        new_water_demand = baseline_infrastructure.get("water_demand", 100) * (1 + surge_pct * 0.8)
        new_waste_gen = baseline_infrastructure.get("waste_volume", 100) * (1 + surge_pct * 1.2)
        
        return {
            "scenario": "Tourism Surge",
            "impacts": {
                "traffic_pressure_index": new_traffic_pressure,
                "water_demand_index": new_water_demand,
                "waste_generation_index": new_waste_gen
            },
            "infrastructure_warnings": ["Traffic exceeds capacity", "Waste management requires overflow routing"] if new_traffic_pressure > 120 else []
        }
