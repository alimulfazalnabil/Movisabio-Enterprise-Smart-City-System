from typing import Dict, Any

class EmissionEstimator:
    """
    Transforms traffic states into emission estimates for environmental intelligence.
    """
    
    def estimate_corridor_emissions(self, traffic_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates an estimated emission risk level based on stop-and-go patterns.
        """
        avg_speed = traffic_state.get('average_speed_kmh', 50)
        idle_time_pct = traffic_state.get('idle_time_pct', 0)
        stop_events_per_km = traffic_state.get('stop_events_per_km', 0)
        
        # Stop-and-go index (simplified heuristic)
        # Higher idle time, higher stops per km, lower average speed -> higher emissions
        stop_and_go_index = (idle_time_pct * 0.5) + (stop_events_per_km * 2.0) - (avg_speed * 0.1)
        
        emission_level = "NORMAL"
        if stop_and_go_index > 20:
            emission_level = "CRITICAL"
        elif stop_and_go_index > 10:
            emission_level = "ELEVATED"
            
        return {
            "corridor_id": traffic_state.get("corridor_id"),
            "stop_and_go_index": max(0, stop_and_go_index),
            "estimated_emission_level": emission_level,
            "is_estimated": True
        }
