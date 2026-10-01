import pytest
from datetime import datetime, timezone
from src.services.network.models.schemas import RoadSegment, Corridor
from src.services.network.engine.graph import TrafficNetworkGraph

def test_graph_topology():
    graph = TrafficNetworkGraph()
    
    seg1 = RoadSegment(
        segment_id="S1", source_intersection_id="I1", target_intersection_id="I2",
        length_meters=200, capacity_vph=1000, current_flow=500, current_speed=15.0,
        queue_length_meters=0.0, timestamp=datetime.now(timezone.utc)
    )
    seg2 = RoadSegment(
        segment_id="S2", source_intersection_id="I2", target_intersection_id="I3",
        length_meters=200, capacity_vph=1000, current_flow=500, current_speed=15.0,
        queue_length_meters=0.0, timestamp=datetime.now(timezone.utc)
    )
    
    graph.add_segment(seg1)
    graph.add_segment(seg2)
    
    assert len(graph.get_downstream_segment("I1")) == 1
    assert graph.get_downstream_segment("I1")[0].segment_id == "S1"
    
    assert len(graph.get_upstream_segment("I2")) == 1
    assert graph.get_upstream_segment("I2")[0].segment_id == "S1"
    
    assert len(graph.get_downstream_segment("I2")) == 1
    assert graph.get_downstream_segment("I2")[0].segment_id == "S2"
