import pytest
from src.services.industrial.engine.oee import OEEEngine

def test_oee_calculation():
    engine = OEEEngine()
    
    # 8h shift (480 min), 40 min downtime -> 440 min operating time
    # Ideal cycle = 1.0 min/part
    # Total count = 400 parts
    # Good count = 380 parts
    
    data = engine.calculate_oee(
        planned_time=480.0,
        operating_time=440.0,
        ideal_cycle_time=1.0,
        total_count=400,
        good_count=380
    )
    
    # Availability = 440 / 480 = 0.916...
    assert data.availability == pytest.approx(0.917)
    
    # Performance = (1.0 * 400) / 440 = 0.909...
    assert data.performance == pytest.approx(0.909)
    
    # Quality = 380 / 400 = 0.95
    assert data.quality == pytest.approx(0.950)
    
    # OEE = 0.916... * 0.909... * 0.95 = 0.791...
    assert data.overall_oee == pytest.approx(0.792)
