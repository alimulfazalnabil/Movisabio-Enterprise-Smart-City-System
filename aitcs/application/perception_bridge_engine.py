"""Buffer vehicle perception telemetry and derive immediate safety flags."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class PerceptionTelemetryRecord:
    """Normalized sensor-fusion record received from one vehicle."""

    intersection_id: str
    vehicle_id: str
    lane_departure_detected: bool
    curvature_radius: float
    collision_risk_score: float
    fused_objects_count: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PerceptionBridgeEngine:
    """Keep recent frames in memory and evaluate simple alert thresholds."""

    def __init__(self) -> None:
        """Create an empty process-local history capped at 2,000 records."""

        self.telemetry_history: list[PerceptionTelemetryRecord] = []

    def process_perception_frame(
        self,
        intersection_id: str,
        vehicle_id: str,
        lane_departure: bool,
        curvature: float,
        risk_score: float,
        objects_count: int,
    ) -> PerceptionTelemetryRecord:
        """Store one perception frame and return its normalized record.

        Older records are discarded once the in-memory cap is reached. The
        history is neither persistent nor shared between worker processes.
        """
        record = PerceptionTelemetryRecord(
            intersection_id=intersection_id,
            vehicle_id=vehicle_id,
            lane_departure_detected=lane_departure,
            curvature_radius=curvature,
            collision_risk_score=risk_score,
            fused_objects_count=objects_count,
        )
        self.telemetry_history.append(record)
        if len(self.telemetry_history) > 2000:
            self.telemetry_history.pop(0)
        return record

    def evaluate_safety_threshold(
        self, record: PerceptionTelemetryRecord
    ) -> dict[str, Any]:
        """Classify a record and return the recommended monitoring action."""
        critical_alert = (
            record.collision_risk_score > 0.75
            or record.lane_departure_detected
        )
        action_required = (
            "EMERGENCY_BRAKING_RECOMMENDED"
            if record.collision_risk_score > 0.85
            else "NORMAL_MONITORING"
        )

        return {
            "vehicle_id": record.vehicle_id,
            "intersection_id": record.intersection_id,
            "critical_alert": critical_alert,
            "recommended_action": action_required,
            "timestamp": record.timestamp,
        }
