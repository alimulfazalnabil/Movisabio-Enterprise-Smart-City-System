"""Convert raw intersection telemetry into a normalized traffic snapshot."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Any
from aitcs.domain.value_objects import GranularTrafficState, LevelOfService


class TrafficStateEstimationService:
    """Estimate traffic indicators with deterministic, configurable heuristics."""

    def __init__(
        self, free_flow_speed_kmh: float = 50.0, max_queue_meters: float = 250.0
    ):
        """Set the reference speed and queue length used for normalization."""

        self.free_flow_speed_kmh = free_flow_speed_kmh
        self.max_queue_meters = max_queue_meters

    def estimate_state(
        self, intersection_id: str, raw_telemetry: Dict[str, Any]
    ) -> GranularTrafficState:
        """Normalize a telemetry mapping and calculate congestion indicators.

        Args:
            intersection_id: Identifier copied to the resulting snapshot.
            raw_telemetry: Counts and measurements using the keys read below.
                Missing values fall back to zero or the configured free-flow
                speed.

        Returns:
            A new traffic snapshot with delay, level of service, congestion and
            pressure estimates.
        """
        vehicle_count = int(raw_telemetry.get("vehicle_count", 0))
        pedestrian_count = int(raw_telemetry.get("pedestrian_count", 0))
        occupancy = float(raw_telemetry.get("occupancy_percentage", 0.0))
        queue_length = float(raw_telemetry.get("queue_length_meters", 0.0))
        avg_speed = float(
            raw_telemetry.get("average_speed_kmh", self.free_flow_speed_kmh)
        )
        max_speed = float(raw_telemetry.get("max_speed_kmh", self.free_flow_speed_kmh))

        turning_left = int(raw_telemetry.get("turning_left_count", 0))
        turning_right = int(raw_telemetry.get("turning_right_count", 0))
        straight = int(raw_telemetry.get("straight_count", 0))

        speed_ratio = max(0.05, avg_speed / self.free_flow_speed_kmh)
        delay_seconds = max(2.0, (1.0 - speed_ratio) * 60.0 + (queue_length / 5.0))
        los = self._calculate_los(delay_seconds)

        queue_ratio = min(1.0, queue_length / self.max_queue_meters)
        speed_degradation = max(0.0, 1.0 - speed_ratio)
        congestion_index = round(
            0.4 * queue_ratio + 0.4 * speed_degradation + 0.2 * (occupancy / 100.0), 4
        )
        congestion_index = min(1.0, max(0.0, congestion_index))

        pressure = round(queue_length * 1.5 + vehicle_count * 0.8, 2)
        travel_time_seconds = (0.5 / max(5.0, avg_speed)) * 3600.0

        return GranularTrafficState(
            intersection_id=intersection_id,
            vehicle_count=vehicle_count,
            pedestrian_count=pedestrian_count,
            lane_occupancy_percentage=occupancy,
            queue_length_meters=queue_length,
            average_speed_kmh=avg_speed,
            max_speed_kmh=max_speed,
            turning_left_count=turning_left,
            turning_right_count=turning_right,
            straight_count=straight,
            estimated_travel_time_seconds=round(travel_time_seconds, 2),
            delay_seconds=round(delay_seconds, 2),
            level_of_service=los,
            congestion_index=congestion_index,
            intersection_pressure=pressure,
            timestamp=datetime.utcnow(),
        )

    def _calculate_los(self, delay: float) -> LevelOfService:
        """Map average delay in seconds to a level-of-service grade."""
        if delay <= 10.0:
            return LevelOfService.A
        elif delay <= 20.0:
            return LevelOfService.B
        elif delay <= 35.0:
            return LevelOfService.C
        elif delay <= 55.0:
            return LevelOfService.D
        elif delay <= 80.0:
            return LevelOfService.E
        else:
            return LevelOfService.F
