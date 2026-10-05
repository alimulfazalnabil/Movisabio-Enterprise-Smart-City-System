import pytest
from src.services.maas.engine.routing import MultimodalRoutingEngine

def test_routing_objectives():
    engine = MultimodalRoutingEngine()
    
    # Fastest should prioritize the ride-hailing plan (less time, higher cost)
    plans_fast = engine.generate_alternatives("A", "B", objective="FASTEST")
    assert plans_fast[0].transfers == 0
    assert plans_fast[0].total_travel_time_sec == 1200
    
    # Cheapest should prioritize the transit plan (more time, lower cost)
    plans_cheap = engine.generate_alternatives("A", "B", objective="CHEAPEST")
    assert plans_cheap[0].transfers == 1
    assert plans_cheap[0].total_cost == 2.40
