from src.services.buildings.models.schemas import ZoneOccupancy

class OccupancyEngine:
    """
    Estimates building occupancy and calculates comfort scores.
    """
    
    def evaluate_zone(self, zone: ZoneOccupancy, temperature: float, co2_ppm: float) -> ZoneOccupancy:
        """
        Calculates comfort score based on temperature, CO2, and occupancy.
        """
        # Base comfort
        comfort = 1.0
        
        # Temp penalty
        if temperature < 20.0 or temperature > 24.0:
            comfort -= 0.2
            
        # CO2 penalty
        if co2_ppm > 1000:
            comfort -= 0.3
        elif co2_ppm > 800:
            comfort -= 0.1
            
        # Overcrowding penalty
        utilization = zone.estimated_occupancy / zone.max_capacity if zone.max_capacity > 0 else 1.0
        if utilization > 0.9:
            comfort -= 0.2
            
        zone.comfort_score = max(0.0, round(comfort, 2))
        return zone
