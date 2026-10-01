import pytest
from datetime import datetime, timedelta
from src.services.perception.trajectory.models import TrajectoryPoint
from src.services.perception.trajectory.speed import SpeedEstimator

def test_speed_calculation():
    estimator = SpeedEstimator()
    
    p1 = TrajectoryPoint(
        timestamp=datetime(2026, 1, 1, 10, 0, 0, 0),
        image_x=100, image_y=100,
        world_x=0.0, world_y=0.0,
        confidence=1.0
    )
    
    p2 = TrajectoryPoint(
        timestamp=datetime(2026, 1, 1, 10, 0, 1, 0), # 1 second later
        image_x=110, image_y=110,
        world_x=10.0, world_y=0.0, # Moved 10 meters in 1 second
        confidence=1.0
    )
    
    speed_kmh = estimator.calculate_instantaneous_speed(p1, p2)
    assert speed_kmh == 36.0 # 10 m/s is 36 km/h
    
def test_acceleration_calculation():
    estimator = SpeedEstimator()
    accel = estimator.calculate_acceleration(36.0, 72.0, 2.0)
    # 10 m/s to 20 m/s in 2 seconds = 5 m/s^2
    assert accel == 5.0
