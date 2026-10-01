from typing import List, Tuple
from pydantic import BaseModel

class LaneDefinition(BaseModel):
    """
    Geospatial definition of a physical traffic lane.
    """
    lane_id: str
    polygon: List[Tuple[float, float]]  # List of points forming the bounding polygon
    direction: str  # NORTH, SOUTH, EAST, WEST
    movement: str   # STRAIGHT, LEFT_TURN, RIGHT_TURN, U_TURN

class IntersectionGeometry(BaseModel):
    intersection_id: str
    lanes: List[LaneDefinition]
