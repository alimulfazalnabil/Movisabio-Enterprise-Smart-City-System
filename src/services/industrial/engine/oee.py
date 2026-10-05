from src.services.industrial.models.schemas import OEEData

class OEEEngine:
    """
    Calculates Overall Equipment Effectiveness (OEE).
    """
    
    def calculate_oee(self, planned_time: float, operating_time: float, ideal_cycle_time: float, total_count: int, good_count: int) -> OEEData:
        """
        Availability = Operating Time / Planned Production Time
        Performance = (Ideal Cycle Time * Total Count) / Operating Time
        Quality = Good Count / Total Count
        OEE = Availability * Performance * Quality
        """
        availability = operating_time / planned_time if planned_time > 0 else 0.0
        performance = (ideal_cycle_time * total_count) / operating_time if operating_time > 0 else 0.0
        quality = good_count / total_count if total_count > 0 else 0.0
        
        oee = availability * performance * quality
        
        return OEEData(
            availability=round(availability, 3),
            performance=round(performance, 3),
            quality=round(quality, 3),
            overall_oee=round(oee, 3)
        )
