from typing import Dict, List, Optional
from src.services.network.models.schemas import RoadSegment, Corridor

class TrafficNetworkGraph:
    """
    Maintains the network state of intersections and road segments.
    """
    def __init__(self):
        self.segments: Dict[str, RoadSegment] = {}
        self.corridors: Dict[str, Corridor] = {}
        
    def add_segment(self, segment: RoadSegment):
        self.segments[segment.segment_id] = segment
        
    def add_corridor(self, corridor: Corridor):
        self.corridors[corridor.corridor_id] = corridor
        
    def get_downstream_segment(self, intersection_id: str) -> List[RoadSegment]:
        return [s for s in self.segments.values() if s.source_intersection_id == intersection_id]
        
    def get_upstream_segment(self, intersection_id: str) -> List[RoadSegment]:
        return [s for s in self.segments.values() if s.target_intersection_id == intersection_id]
