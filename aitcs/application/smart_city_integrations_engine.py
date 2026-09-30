"""Demonstration adapters for utility status and citizen reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

@dataclass(frozen=True)
class UtilityMonitorRecord:
    """Latest simulated readings for a utility station."""

    station_id: str
    grid_load_mw: float
    transformer_temp_c: float
    status: str

@dataclass(frozen=True)
class CitizenReport:
    """Citizen-submitted issue retained by the local engine process."""

    report_id: str
    category: str  # POTHOLE, STREETLIGHT_FAILURE, TRAFFIC_SIGNAL_OUT, ROAD_OBSTRUCTION
    location_desc: str
    latitude: float
    longitude: float
    status: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

class SmartCityIntegrationsEngine:
    """Expose simulated utility data and an in-memory citizen report inbox."""

    def __init__(self):
        """Create an empty process-local citizen report list."""

        self.citizen_reports: List[CitizenReport] = []

    def monitor_utility_grid(self, station_id: str) -> UtilityMonitorRecord:
        """Return fixed demonstration readings labelled with ``station_id``."""
        return UtilityMonitorRecord(
            station_id=station_id,
            grid_load_mw=42.5,
            transformer_temp_c=68.4,
            status="STABLE"
        )

    def submit_citizen_report(self, category: str, description: str, latitude: float, longitude: float) -> CitizenReport:
        """Create, store and return a citizen report.

        Reports are not persisted and IDs use the current time to the second, so
        callers must not assume global uniqueness.
        """
        report = CitizenReport(
            report_id=f"CIT-{datetime.utcnow().strftime('%H%M%S')}",
            category=category.upper(),
            location_desc=description,
            latitude=latitude,
            longitude=longitude,
            status="RECEIVED"
        )
        self.citizen_reports.append(report)
        return report
