"""Calculate pedestrian clearance time from crowd and vulnerability counts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class PedestrianState:
    """Observed demand and recommended crossing duration for one crossing."""

    intersection_id: str
    waiting_count: int
    elderly_or_disabled_count: int
    school_crossing_active: bool
    recommended_crossing_duration_seconds: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

class PedestrianIntelligenceEngine:
    """Apply deterministic bonuses to a base pedestrian clearance time."""

    def calculate_crossing_timing(
        self, intersection_id: str, waiting_count: int, elderly_count: int = 0, school_mode: bool = False
    ) -> PedestrianState:
        """Recommend a crossing duration in seconds.

        School mode raises the base duration, each five waiting pedestrians add
        one second up to 20, and each vulnerable pedestrian adds three seconds.
        """
        base_time = 15  # standard pedestrian clearance seconds
        if school_mode:
            base_time = 25

        # Adapt crossing duration for dense crowds or vulnerable pedestrians with slower crossing speeds
        density_bonus = min(20, waiting_count // 5)
        vulnerability_bonus = elderly_count * 3

        total_duration = base_time + density_bonus + vulnerability_bonus

        return PedestrianState(
            intersection_id=intersection_id,
            waiting_count=waiting_count,
            elderly_or_disabled_count=elderly_count,
            school_crossing_active=school_mode,
            recommended_crossing_duration_seconds=total_duration
        )
