import pytest
from src.services.maas.engine.booking import MaaSBookingEngine
from src.services.maas.engine.routing import MultimodalRoutingEngine

def test_fare_calculation():
    routing = MultimodalRoutingEngine()
    booking = MaaSBookingEngine()
    
    # Get a dummy plan
    plans = routing.generate_alternatives("A", "B")
    transit_plan = next(p for p in plans if p.transfers == 1)
    
    assert transit_plan.total_cost == 2.40
    
    # Apply a 10% MaaS subscription discount
    discounted_fare = booking.calculate_total_fare(transit_plan, discount_rate=0.1)
    
    assert discounted_fare == pytest.approx(2.16)
