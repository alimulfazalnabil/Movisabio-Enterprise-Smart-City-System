from typing import Dict, Any, List

class AgricultureIntelligenceEngine:
    """
    B18 - Food, Agriculture, Fisheries, Blue Economy & Rural Territorial Intelligence
    Models the rural production chain and food security.
    """

    def forecast_crop_yield(self, crop: Dict[str, Any], weather: Dict[str, Any], soil: Dict[str, Any]) -> Dict[str, Any]:
        """
        B18.11 - Yield Forecasting
        Estimates the final yield based on current crop health and expected weather.
        """
        base_yield = crop.get("expected_yield_tonnes", 100)
        
        # Penalize for bad weather
        weather_penalty = 1.0
        if weather.get("drought_index", 0) > 0.7:
            weather_penalty = 0.85
            
        # Penalize for poor soil
        soil_penalty = 1.0
        if soil.get("moisture_pct", 50) < 30:
            soil_penalty = 0.90
            
        forecast = base_yield * weather_penalty * soil_penalty
        
        return {
            "forecast_yield_tonnes": round(forecast, 1),
            "confidence_pct": 82.5,
            "risk_factors": ["Drought" if weather_penalty < 1 else None]
        }

    def analyze_cold_chain(self, telemetry: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B18.21 - Cold-Chain Intelligence
        Evaluates a series of temperature readings across a logistics route.
        """
        excursions = 0
        max_temp = -999
        
        for reading in telemetry:
            t = reading.get("temperature_c", 0)
            target = reading.get("target_c", 4)
            if t > target + 2:
                excursions += 1
            if t > max_temp:
                max_temp = t
                
        spoilage_risk = excursions * 5.0 # Mock metric
        
        return {
            "status": "COMPROMISED" if excursions > 0 else "INTACT",
            "excursion_events": excursions,
            "max_recorded_temp_c": max_temp,
            "estimated_spoilage_pct": min(100.0, spoilage_risk)
        }

    def evaluate_rural_infrastructure(self, location: Dict[str, Any], roads: List[Dict[str, Any]], markets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B18.25 - Rural Infrastructure Intelligence
        Scores how well-connected a rural production node is to the broader economy.
        """
        # Simplistic mock: distance to nearest market and condition of nearest road
        road_score = sum(r.get("condition_score", 50) for r in roads) / max(1, len(roads))
        
        return {
            "rural_accessibility_index": round(road_score * 0.8, 1), # Max 80 just based on roads
            "bottlenecks": ["Poor road condition detected on access route"] if road_score < 40 else [],
            "market_access": "ADEQUATE" if len(markets) > 0 else "ISOLATED"
        }
