"""Immutable values exchanged by traffic estimation and decision engines."""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

class LevelOfService(str, Enum):
    """Highway level-of-service grade, from free flow (A) to breakdown (F)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

@dataclass(frozen=True)
class GranularTrafficState:
    """Normalized snapshot of traffic conditions at one intersection."""

    intersection_id: str
    vehicle_count: int
    pedestrian_count: int
    lane_occupancy_percentage: float
    queue_length_meters: float
    average_speed_kmh: float
    max_speed_kmh: float
    turning_left_count: int
    turning_right_count: int
    straight_count: int
    estimated_travel_time_seconds: float
    delay_seconds: float
    level_of_service: LevelOfService
    congestion_index: float
    intersection_pressure: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
