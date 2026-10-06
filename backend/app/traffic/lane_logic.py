from shapely.geometry import Point, Polygon, LineString
from typing import List, Dict

from backend.app.traffic.perception import Track

class LaneConfig:
    def __init__(self, lane_id: str, direction: str, movement: str, polygon: List[List[float]], speed_limit: float, crossing_line: List[List[float]] = None):
        self.lane_id = lane_id
        self.direction = direction
        self.movement = movement
        self.polygon = Polygon(polygon) if len(polygon) >= 3 else None
        self.speed_limit = speed_limit
        self.crossing_line = LineString(crossing_line) if crossing_line else None

class LaneManager:
    def __init__(self, lanes: List[LaneConfig]):
        self.lanes = lanes
        self.flow_counts = {lane.lane_id: 0 for lane in lanes}
        self.crossed_tracks = {lane.lane_id: set() for lane in lanes}

    def assign_lane(self, track: Track) -> str | None:
        pt = Point(track.center[0], track.center[1])
        for lane in self.lanes:
            if lane.polygon and lane.polygon.contains(pt):
                return lane.lane_id
        return None

    def process_tracks(self, tracks: List[Track]) -> Dict[str, dict]:
        # Reset instantaneous counts
        lane_state = {lane.lane_id: {"instantaneous_count": 0, "flow_count": self.flow_counts[lane.lane_id]} for lane in self.lanes}
        
        for track in tracks:
            assigned_lane_id = self.assign_lane(track)
            if assigned_lane_id:
                lane_state[assigned_lane_id]["instantaneous_count"] += 1
                
                # Check for line crossing if trajectory has at least 2 points
                if len(track.trajectory) >= 2:
                    p1, p2 = track.trajectory[-2], track.trajectory[-1]
                    track_line = LineString([p1, p2])
                    lane = next((l for l in self.lanes if l.lane_id == assigned_lane_id), None)
                    if lane and lane.crossing_line and track.track_id not in self.crossed_tracks[assigned_lane_id]:
                        if track_line.intersects(lane.crossing_line):
                            self.flow_counts[assigned_lane_id] += 1
                            self.crossed_tracks[assigned_lane_id].add(track.track_id)
                            lane_state[assigned_lane_id]["flow_count"] = self.flow_counts[assigned_lane_id]
                            
        return lane_state
