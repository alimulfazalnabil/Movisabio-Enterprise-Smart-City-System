"""Detect rule-based traffic incidents and describe emergency corridors."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass(frozen=True)
class IncidentAlert:
    """Detected incident and the evidence link exposed to operators."""

    incident_id: str
    intersection_id: str
    incident_type: str  # ACCIDENT, STOPPED_VEHICLE, WRONG_WAY, ROAD_BLOCKAGE
    severity: str       # LOW, MEDIUM, CRITICAL
    description: str
    snapshot_url: Optional[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class EmergencyCorridorPlan:
    """Ordered intersections and forced green time for a response corridor."""

    corridor_id: str
    emergency_type: str # AMBULANCE, FIRE, POLICE
    intersection_sequence: List[str]
    forced_green_seconds: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

class IncidentEmergencyEngine:
    """Evaluate telemetry rules and retain detected incidents in memory."""

    def __init__(self):
        """Create an empty process-local incident list."""

        self.active_incidents: List[IncidentAlert] = []

    def detect_incidents(self, intersection_id: str, telemetry: dict) -> List[IncidentAlert]:
        """Create alerts for wrong-way travel and clustered sudden stoppages.

        The returned alerts are also appended to ``active_incidents``. This
        method performs no deduplication, persistence or external notification.
        """
        alerts = []
        if telemetry.get("wrong_way_detected", False):
            alerts.append(IncidentAlert(
                incident_id=f"INC-{datetime.utcnow().strftime('%H%M%S')}-WW",
                intersection_id=intersection_id,
                incident_type="WRONG_WAY",
                severity="CRITICAL",
                description="Wrong-way driving maneuver detected on approach lane.",
                snapshot_url=f"https://snapshots.movisabio.io/{intersection_id}/wrong_way.jpg"
            ))
        
        if telemetry.get("sudden_stoppage_count", 0) > 3:
            alerts.append(IncidentAlert(
                incident_id=f"INC-{datetime.utcnow().strftime('%H%M%S')}-ACC",
                intersection_id=intersection_id,
                incident_type="ACCIDENT",
                severity="HIGH",
                description="Sudden vehicle cluster stoppage indicative of collision.",
                snapshot_url=f"https://snapshots.movisabio.io/{intersection_id}/collision.jpg"
            ))

        self.active_incidents.extend(alerts)
        return alerts

    def activate_emergency_corridor(self, corridor_id: str, emergency_type: str, sequence: List[str]) -> EmergencyCorridorPlan:
        """Describe a fixed 90-second corridor plan without activating hardware."""
        return EmergencyCorridorPlan(
            corridor_id=corridor_id,
            emergency_type=emergency_type.upper(),
            intersection_sequence=sequence,
            forced_green_seconds=90
        )
