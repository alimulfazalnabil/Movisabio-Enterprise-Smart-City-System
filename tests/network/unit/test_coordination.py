import pytest
from src.services.network.models.schemas import Corridor
from src.services.network.engine.coordination import CorridorCoordinator

def test_corridor_coordination():
    coord = CorridorCoordinator()
    
    corridor = Corridor(
        corridor_id="C1",
        intersections=["I1", "I2", "I3"],
        segments=["S1", "S2"]
    )
    
    # 20m/s speed, length 200m each -> 10s travel time between intersections
    segment_lengths = {"S1": 200.0, "S2": 200.0}
    
    plan = coord.generate_candidate_plan(corridor, base_cycle=60, speed_mps=20.0, segment_lengths=segment_lengths)
    
    assert plan.cycle_length_sec == 60
    assert plan.offsets["I1"] == 0
    assert plan.offsets["I2"] == 10  # 0 + 10
    assert plan.offsets["I3"] == 20  # 10 + 10
