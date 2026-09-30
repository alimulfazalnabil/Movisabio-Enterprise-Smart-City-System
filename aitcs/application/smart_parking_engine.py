"""Read parking occupancy from a built-in, process-local zone registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass(frozen=True)
class ParkingZoneStatus:
    """Capacity and computed availability for one parking zone."""

    zone_id: str
    total_slots: int
    occupied_slots: int
    available_slots: int
    turnover_rate_per_hour: float
    occupancy_percentage: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class SmartParkingEngine:
    """Calculate parking availability from demonstration occupancy values."""

    def __init__(self):
        """Load the built-in parking zones."""

        self.zones: Dict[str, dict] = {
            "PARK-CENTRAL-01": {"total": 150, "occupied": 120, "turnover": 4.5},
            "PARK-COMMERCIAL-02": {"total": 80, "occupied": 25, "turnover": 2.1},
            "PARK-HUB-03": {"total": 250, "occupied": 240, "turnover": 6.8}
        }

    def get_zone_status(self, zone_id: str) -> ParkingZoneStatus:
        """Return capacity and occupancy for a zone.

        Unknown IDs receive a generic 100-space, 50-percent occupied fallback;
        absence is not reported as an error.
        """
        data = self.zones.get(zone_id, {"total": 100, "occupied": 50, "turnover": 3.0})
        total = data["total"]
        occupied = data["occupied"]
        available = max(0, total - occupied)
        pct = round((occupied / total) * 100.0, 2)
        
        return ParkingZoneStatus(
            zone_id=zone_id,
            total_slots=total,
            occupied_slots=occupied,
            available_slots=available,
            turnover_rate_per_hour=data["turnover"],
            occupancy_percentage=pct
        )
