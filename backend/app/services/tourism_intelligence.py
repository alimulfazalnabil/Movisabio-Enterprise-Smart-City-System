from typing import Dict, Any, List

class DestinationIntelligenceEngine:
    """
    B21 - Tourism, Culture, Heritage, Events & Destination Intelligence
    Analyzes capacity, visitor flows, and event impact to manage sustainable tourism.
    """

    def analyze_carrying_capacity(self, visitors: int, physical_cap: int, water_stress: float, resident_sentiment: float) -> Dict[str, Any]:
        """
        B21.6 - Tourism Carrying Capacity & B21.7 Overtourism Intelligence
        Evaluates destination pressure across multiple dimensions.
        """
        pressure = (visitors / max(1, physical_cap)) * 100
        
        status = "NORMAL"
        primary_constraint = None
        
        if pressure > 90:
            status = "OVERTOURISM"
            primary_constraint = "Physical Capacity"
        elif water_stress > 0.85:
            status = "ENVIRONMENTAL_STRESS"
            primary_constraint = "Water Infrastructure"
        elif resident_sentiment < 0.4: # 0 to 1 scale
            status = "SOCIAL_STRESS"
            primary_constraint = "Resident Tolerance"
            
        return {
            "current_pressure_pct": round(pressure, 1),
            "status": status,
            "primary_bottleneck": primary_constraint,
            "recommendation": "Activate dynamic routing to alternative attractions." if status != "NORMAL" else "Continue monitoring."
        }

    def assess_heritage_risk(self, site: Dict[str, Any], environmental_data: Dict[str, Any], visitor_flow: int) -> Dict[str, Any]:
        """
        B21.12 - Heritage Conservation Intelligence
        Monitors a heritage asset against environmental and human pressure.
        """
        base_status = site.get("conservation_status", "INTACT")
        vibrations = environmental_data.get("vibration_index", 0)
        humidity = environmental_data.get("humidity_pct", 50)
        
        risk_score = 0
        if vibrations > 70:
            risk_score += 40
        if humidity > 85:
            risk_score += 20
        if visitor_flow > 5000:
            risk_score += 20
            
        return {
            "site_id": site.get("site_id", "UNKNOWN"),
            "conservation_risk_score": risk_score,
            "immediate_threat": "Traffic Vibrations" if vibrations > 70 else None,
            "action_required": risk_score > 50
        }

    def generate_dynamic_routing(self, congested_attraction_id: str, alternatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        B21.8 - Dynamic Visitor Distribution
        Recommends alternative attractions when a primary site is overloaded.
        """
        # Sort alternatives by current capacity (lowest first)
        sorted_alts = sorted(alternatives, key=lambda x: x.get("current_visitor_count", 0) / max(1, x.get("max_daily_capacity", 1)))
        
        # Return top 2 recommendations
        return [
            {
                "attraction_name": alt.get("name"),
                "available_capacity_pct": 100 - (alt.get("current_visitor_count", 0) / max(1, alt.get("max_daily_capacity", 1)) * 100)
            }
            for alt in sorted_alts[:2]
        ]
