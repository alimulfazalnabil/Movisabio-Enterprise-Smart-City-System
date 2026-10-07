from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter()

# B21.30 - Destination APIs
@router.post("/destinations/scenarios", response_model=Dict[str, Any])
def simulate_destination_scenario(scenario: Dict[str, Any]):
    """B21.31 - Destination Capacity & Sustainable Tourism Digital Twin"""
    visitor_growth = scenario.get("visitor_growth", 0.0)
    
    impact = "MODERATE"
    if visitor_growth > 0.20:
        impact = "HIGH"
    elif visitor_growth > 0.40:
        impact = "SEVERE_OVERTOURISM"
        
    return {
        "scenario": scenario.get("scenario", "Custom Growth"),
        "visitor_demand_surge_pct": visitor_growth * 100,
        "infrastructure_pressure": impact,
        "mobility_impact": f"{int(visitor_growth * 150)}% increase in peak congestion",
        "environmental_impact": "Water demand exceeds sustainable extraction limits" if visitor_growth > 0.25 else "Within limits",
        "capacity_constraints": ["Parking capacity", "Waste management"],
        "confidence": 0.88,
        "recommendation": "Implement dynamic pricing and promote alternative tourism zones."
    }

@router.get("/heritage/risk", response_model=Dict[str, Any])
def get_heritage_conservation_risk():
    """B21.12 - Heritage Conservation Intelligence"""
    return {
        "status": "MONITORING",
        "at_risk_sites": [
            {
                "site_name": "Old City Walls",
                "primary_risk": "Vibration from heavy traffic",
                "recommended_action": "Reroute heavy vehicles; trigger structural inspection."
            }
        ]
    }

@router.post("/events/forecast", response_model=Dict[str, Any])
def forecast_event_impact(event: Dict[str, Any]):
    """B21.16 - Event Attendance Forecasting"""
    expected = event.get("expected_attendance", 10000)
    return {
        "event": event.get("name", "Unknown Event"),
        "forecasted_attendance": expected,
        "transit_demand_surge": expected * 0.6, # Assuming 60% use transit
        "security_risk_level": "ELEVATED" if expected > 50000 else "NORMAL"
    }
