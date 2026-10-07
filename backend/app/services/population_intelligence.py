from typing import Dict, Any, List

class PopulationIntelligenceEngine:
    """
    B35 - Population, Demographic, Migration & Human Mobility Intelligence
    Models population changes, migration flows, and service demands.
    """

    def forecast_population(self, current_population: int, fertility_rate: float, mortality_rate: float, net_migration: int) -> Dict[str, Any]:
        """
        B35.4 - Population Forecasting
        Simple cohort-component projection step for a single period.
        """
        natural_increase = current_population * (fertility_rate - mortality_rate)
        projected_population = int(current_population + natural_increase + net_migration)
        
        return {
            "current_population": current_population,
            "projected_population": projected_population,
            "natural_increase": int(natural_increase),
            "net_migration": net_migration,
            "growth_rate_pct": round(((projected_population / current_population) - 1) * 100, 2)
        }

    def project_service_demand(self, demographic_segment_size: int, utilization_rate_per_capita: float, current_capacity: float) -> Dict[str, Any]:
        """
        B35.12 - Population-Service Demand Model
        Projects the demand for a specific service (e.g. elderly care) based on population segments.
        """
        projected_demand = demographic_segment_size * utilization_rate_per_capita
        capacity_gap = max(0.0, projected_demand - current_capacity)
        
        return {
            "demographic_segment_size": demographic_segment_size,
            "projected_demand": round(projected_demand, 2),
            "current_capacity": current_capacity,
            "capacity_gap": round(capacity_gap, 2),
            "status": "DEFICIT" if capacity_gap > 0 else "SUFFICIENT"
        }

    def analyze_urbanization_pressure(self, migration_volume: int, available_housing_units: int, household_size: float) -> Dict[str, Any]:
        """
        B35.7 - Urbanization Intelligence
        Models housing and infrastructure pressure caused by inward migration.
        """
        new_households_needed = migration_volume / household_size
        housing_deficit = max(0.0, new_households_needed - available_housing_units)
        
        return {
            "migration_volume": migration_volume,
            "new_households_needed": round(new_households_needed, 1),
            "housing_deficit": round(housing_deficit, 1),
            "pressure_level": "HIGH" if housing_deficit > (available_housing_units * 0.1) else "MANAGEABLE"
        }
