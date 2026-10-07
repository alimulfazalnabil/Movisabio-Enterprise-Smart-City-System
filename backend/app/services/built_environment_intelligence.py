from typing import Dict, Any, List

class BuiltEnvironmentIntelligenceEngine:
    """
    B23 - Buildings, Campuses, Facilities & Built-Environment Territorial Intelligence
    Analyzes occupancy, building energy, retrofits, and smart campus simulations.
    """

    def simulate_campus_impact(self, current_state: Dict[str, Any], occupancy_multiplier: float) -> Dict[str, Any]:
        """
        B23.39 - Smart Campus Digital Twin
        Simulates the effect of an occupancy surge on campus utilities and mobility.
        """
        base_hvac_kw = current_state.get("hvac_load_kw", 1000)
        base_water_lpd = current_state.get("water_demand_lpd", 50000)
        
        # Simplified non-linear scaling for HVAC
        new_hvac_kw = base_hvac_kw * (1 + (occupancy_multiplier - 1) * 0.8)
        new_water_lpd = base_water_lpd * occupancy_multiplier
        
        return {
            "scenario": f"{int((occupancy_multiplier - 1) * 100)}% Occupancy Increase",
            "projected_hvac_load_kw": round(new_hvac_kw, 1),
            "projected_water_demand_lpd": round(new_water_lpd, 1),
            "parking_impact": "SEVERE_CONGESTION" if occupancy_multiplier > 1.25 else "NORMAL",
            "recommendation": "Activate peak shaving if HVAC load exceeds 1500 kW."
        }

    def evaluate_building_retrofit(self, building_data: Dict[str, Any], budget: float) -> Dict[str, Any]:
        """
        B23.30 - Building Retrofit Intelligence
        Recommends energy retrofits based on ROI and budget constraints.
        """
        energy_intensity = building_data.get("energy_intensity_kwh_sqm", 250)
        
        portfolio = []
        savings_pct = 0.0
        cost = 0.0
        
        if budget >= 50000 and energy_intensity > 200:
            portfolio.append("HVAC Controls Upgrade")
            savings_pct += 15.0
            cost += 45000
            
        if budget - cost >= 20000:
            portfolio.append("LED Lighting Transition")
            savings_pct += 8.0
            cost += 18000
            
        return {
            "recommended_portfolio": portfolio,
            "estimated_cost": cost,
            "remaining_budget": budget - cost,
            "projected_energy_savings_pct": savings_pct,
            "payback_period_years": 4.5 if portfolio else 0.0
        }

    def predict_asset_failure(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        B23.16 - Predictive Maintenance for Building Assets
        Evaluates HVAC/Pump sensor data to predict Remaining Useful Life.
        """
        temp = telemetry.get("compressor_temp_c", 60)
        vibration = telemetry.get("vibration_mm_s", 2.0)
        
        risk_score = 0
        if temp > 85:
            risk_score += 40
        if vibration > 5.0:
            risk_score += 30
            
        return {
            "asset_id": telemetry.get("asset_id"),
            "anomaly_probability": round(risk_score / 100.0, 2),
            "action_required": risk_score >= 50,
            "recommendation": "Dispatch maintenance technician for inspection." if risk_score >= 50 else "Normal operations."
        }
