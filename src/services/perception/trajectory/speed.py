import math
from src.services.perception.trajectory.models import TrajectoryPoint

class SpeedEstimator:
    """
    Translates physical world coordinates between consecutive frames into 
    smoothed velocity and acceleration representations.
    """
    
    def __init__(self, smoothing_alpha: float = 0.8):
        self.smoothing_alpha = smoothing_alpha

    def calculate_instantaneous_speed(self, p1: TrajectoryPoint, p2: TrajectoryPoint) -> float:
        """
        Calculate raw speed in km/h between two TrajectoryPoints in world coordinates.
        """
        dt = (p2.timestamp - p1.timestamp).total_seconds()
        if dt <= 0:
            return 0.0
            
        dx = p2.world_x - p1.world_x
        dy = p2.world_y - p1.world_y
        
        distance_meters = math.sqrt(dx*dx + dy*dy)
        speed_ms = distance_meters / dt
        
        return speed_ms * 3.6
        
    def filter_speed(self, current_raw_speed: float, previous_filtered_speed: float) -> float:
        """
        Apply Exponential Moving Average (EMA) to reduce bounding box jitter.
        """
        return (self.smoothing_alpha * current_raw_speed) + ((1 - self.smoothing_alpha) * previous_filtered_speed)
        
    def calculate_acceleration(self, v1_kmh: float, v2_kmh: float, dt_seconds: float) -> float:
        """
        Calculates acceleration in m/s^2.
        """
        if dt_seconds <= 0:
            return 0.0
            
        v1_ms = v1_kmh / 3.6
        v2_ms = v2_kmh / 3.6
        
        return (v2_ms - v1_ms) / dt_seconds
