from typing import Dict, Any, List
from datetime import datetime, timezone

class SmartChargingEngine:
    """
    Optimizes EV charging based on departure times, grid constraints, and renewable energy.
    """
    
    def calculate_charging_power(self, 
                               vehicle_soc: float, 
                               target_soc: float, 
                               battery_capacity_kwh: float,
                               departure_time: datetime,
                               available_capacity_kw: float,
                               max_charger_power_kw: float) -> float:
        """
        Determines how much power should be allocated to a vehicle to reach 
        its target SOC by departure time, without violating grid or charger constraints.
        """
        if vehicle_soc >= target_soc or vehicle_soc < 0:
            return 0.0
            
        now = datetime.now(timezone.utc)
        time_until_departure_hours = (departure_time - now).total_seconds() / 3600.0
        
        if time_until_departure_hours <= 0:
            return 0.0
            
        energy_needed_kwh = (target_soc - vehicle_soc) / 100.0 * battery_capacity_kwh
        
        # Minimum constant power required to hit target
        required_power_kw = energy_needed_kwh / time_until_departure_hours
        
        # Cap at equipment and grid limits
        allocated_power = min(required_power_kw, max_charger_power_kw, available_capacity_kw)
        
        return allocated_power
