from src.services.tourism.models.schemas import AttractionCapacity

class DestinationEngine:
    def evaluate_attraction_capacity(self, capacity: AttractionCapacity) -> str:
        """
        Evaluates the current crowding level of an attraction based on safe capacity thresholds.
        """
        if capacity.safe_capacity == 0:
            return "UNKNOWN"
            
        utilization = capacity.current_visitors / capacity.safe_capacity
        
        if utilization >= 0.95:
            return "CAPACITY_PRESSURE"
        elif utilization >= 0.80:
            return "HIGH_LOAD"
        elif utilization >= 0.60:
            return "BUSY"
        return "NORMAL"

    def forecast_queue_wait(self, capacity: AttractionCapacity) -> float:
        """
        Estimates the queue wait time in minutes based on net visitor flow.
        """
        net_rate = capacity.entry_rate - capacity.exit_rate
        if net_rate <= 0:
            return 0.0
            
        # Simplified assumption: wait time increases proportionally to the net entry rate
        # and current crowding.
        wait_time = (capacity.current_visitors / capacity.safe_capacity) * net_rate * 2.5
        return round(wait_time, 1)
