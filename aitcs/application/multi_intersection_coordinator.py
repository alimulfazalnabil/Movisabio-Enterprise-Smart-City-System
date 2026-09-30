"""Coordinate offsets along ordered groups of connected intersections."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Set, Tuple

@dataclass(frozen=True)
class GreenWaveCorridor:
    """Progression plan containing one offset per corridor intersection."""

    corridor_id: str
    intersection_sequence: List[str]
    design_speed_kmh: float
    common_cycle_length: int
    calculated_offsets: Dict[str, int]
    bandwidth_percentage: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class MultiIntersectionCoordinator:
    """Store directed road lengths and derive simple green-wave offsets."""

    def __init__(self):
        """Create an empty in-memory road-link registry."""

        self.intersection_graph: Dict[str, Set[str]] = {}
        self.link_distances: Dict[Tuple[str, str], float] = {}

    def register_road_link(self, a: str, b: str, distance_meters: float) -> None:
        """Register the directed distance from intersection ``a`` to ``b``."""
        self.link_distances[(a, b)] = distance_meters

    def design_green_wave_corridor(self, corridor_id: str, sequence: List[str], speed_kmh: float, cycle: int = 90) -> GreenWaveCorridor:
        """Calculate arrival offsets for an ordered intersection sequence.

        Missing links use a 500 metre fallback. ``speed_kmh`` and ``cycle`` must
        be positive; the method currently relies on callers to validate them.
        """
        offsets, dist = {}, 0.0
        speed_mps = speed_kmh * (1000.0 / 3600.0)
        for idx, int_id in enumerate(sequence):
            if idx == 0: offsets[int_id] = 0
            else:
                dist += self.link_distances.get((sequence[idx - 1], int_id), 500.0)
                offsets[int_id] = int(dist / speed_mps) % cycle
        return GreenWaveCorridor(corridor_id, sequence, speed_kmh, cycle, offsets, 75.0)
