from src.services.tourism.models.schemas import AttractionCapacity
from src.services.tourism.engine.destination import DestinationEngine

def test_evaluate_attraction_capacity():
    capacity = AttractionCapacity(
        attraction_id="BEACH-01",
        safe_capacity=1000,
        current_visitors=850,
        entry_rate=15.0,
        exit_rate=10.0
    )
    engine = DestinationEngine()
    status = engine.evaluate_attraction_capacity(capacity)
    assert status == "HIGH_LOAD"

def test_evaluate_capacity_pressure():
    capacity = AttractionCapacity(
        attraction_id="PARK-01",
        safe_capacity=5000,
        current_visitors=4800,
        entry_rate=50.0,
        exit_rate=20.0
    )
    engine = DestinationEngine()
    status = engine.evaluate_attraction_capacity(capacity)
    assert status == "CAPACITY_PRESSURE"

def test_forecast_queue_wait():
    capacity = AttractionCapacity(
        attraction_id="MUSEUM-01",
        safe_capacity=500,
        current_visitors=250,
        entry_rate=10.0,
        exit_rate=5.0
    )
    engine = DestinationEngine()
    wait_time = engine.forecast_queue_wait(capacity)
    # (250/500) * 5.0 * 2.5 = 6.25 -> 6.2
    assert wait_time == 6.2 or wait_time == 6.3
