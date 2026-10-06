from typing import Dict, Any, List

class MobilityOptimizer:
    """
    B9 - Territorial Mobility Intelligence Platform
    Optimizes multi-modal mobility across a territory.
    """
    
    def evaluate_transit_priority(self, transit_vehicle: Dict[str, Any], corridor_state: Dict[str, Any]) -> bool:
        """
        B9.6 - Dynamic Transit Priority
        Evaluate granting signal priority based on delay, load, and traffic impact.
        """
        delay = transit_vehicle.get("delay_seconds", 0)
        load = transit_vehicle.get("occupancy_percentage", 0.0)
        
        # Only prioritize if delayed > 2 mins
        if delay < 120:
            return False
            
        # Example criteria: High occupancy + delay overrides moderate traffic impact
        if load > 0.5:
            # Check traffic impact on corridor
            avg_congestion = corridor_state.get("congestion_level", "MODERATE")
            if avg_congestion in ["SEVERE"]:
                # Do not destabilize an already failing corridor
                return False
            return True
            
        return False

    def optimize_ev_route(self, origin: str, destination: str, vehicle_state: Dict[str, Any], grid_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        B9.15 - EV Route + Charging Optimization
        Optimizes Route + Battery + Charging + Traffic + Energy
        """
        battery = vehicle_state.get("battery_level", 1.0)
        range_km = battery * vehicle_state.get("max_range_km", 400)
        
        if range_km < 50.0:
            # Must route through a charger
            chargers = grid_state.get("available_chargers", [])
            if not chargers:
                return {"status": "NO_AVAILABLE_CHARGERS", "route": None}
                
            selected_charger = chargers[0] # Simplistic greedy choice
            return {
                "status": "CHARGING_REQUIRED",
                "route": [origin, selected_charger["id"], destination],
                "expected_charge_time_min": 25.0
            }
            
        return {
            "status": "DIRECT_ROUTE",
            "route": [origin, destination]
        }

    def optimize_multimodal_route(self, origin: str, destination: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        B9.18 - Multimodal Route Optimization
        """
        optimize_for = preferences.get("objective", "minimum_time")
        
        if optimize_for == "minimum_emissions":
            return {
                "modes": ["WALK", "TRANSIT_RAIL", "WALK"],
                "duration": 55,
                "cost": 2.50,
                "carbon_estimate": 0.2,
                "confidence": 0.95
            }
        elif optimize_for == "minimum_time":
            return {
                "modes": ["RIDE_HAIL"],
                "duration": 25,
                "cost": 15.00,
                "carbon_estimate": 2.5,
                "confidence": 0.88
            }
        else:
            return {
                "modes": ["TRANSIT_BUS", "MICROMOBILITY_SCOOTER"],
                "duration": 40,
                "cost": 3.50,
                "carbon_estimate": 0.6,
                "confidence": 0.90
            }
