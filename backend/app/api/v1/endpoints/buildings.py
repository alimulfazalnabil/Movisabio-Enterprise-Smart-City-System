from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter()

# B23.38 - Building APIs
@router.post("/campuses/scenarios", response_model=Dict[str, Any])
def simulate_campus_scenario(scenario: Dict[str, Any]):
    """B23.39 - Smart Campus Digital Twin Simulation"""
    occupancy_increase = scenario.get("occupancy_increase_pct", 0.0)
    
    return {
        "scenario": scenario.get("scenario", "Occupancy Surge"),
        "simulated_increase_pct": occupancy_increase * 100,
        "hvac_energy_impact_kw": occupancy_increase * 500,
        "water_demand_impact_lpd": occupancy_increase * 10000,
        "parking_capacity_status": "CRITICAL" if occupancy_increase > 0.20 else "MANAGEABLE",
        "recommendation": "Activate peak-shaving for HVAC and incentivize transit." if occupancy_increase > 0.20 else "Normal operations."
    }

@router.post("/buildings/retrofits", response_model=Dict[str, Any])
def optimize_building_retrofit(building: Dict[str, Any]):
    """B23.30 - Building Retrofit Intelligence"""
    budget = building.get("budget", 100000)
    
    return {
        "building_id": building.get("building_id", "BLDG-1"),
        "available_budget": budget,
        "recommended_portfolio": ["HVAC Controls Upgrade", "LED Lighting Transition"],
        "projected_energy_savings_pct": 22.5,
        "payback_period_years": 3.8,
        "carbon_reduction_tons_per_year": 140
    }

@router.get("/assets/maintenance", response_model=Dict[str, Any])
def get_asset_maintenance_alerts():
    """B23.16 - Predictive Maintenance"""
    return {
        "status": "MONITORING",
        "alerts": [
            {
                "asset_id": "CHILLER-02",
                "failure_probability": 0.85,
                "primary_indicator": "High compressor temperature",
                "maintenance_window": "Next 48 hours",
                "recommended_action": "Inspect refrigerant levels and condenser coils."
            }
        ]
    }
