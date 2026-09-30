"""Evaluate transit-signal-priority requests with simple arrival rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class TransitPriorityRequest:
    """Vehicle, route, arrival and occupancy data used by the TSP rule."""

    vehicle_id: str
    transit_type: str  # BUS, BRT, TRAM
    intersection_id: str
    route_number: str
    estimated_arrival_seconds: int
    passenger_count: int

@dataclass(frozen=True)
class TSPDecision:
    """Requested signal action and extension for a transit vehicle."""

    request_id: str
    intersection_id: str
    action_taken: str  # GREEN_EXTENDED, PHASE_HOLD, NONE
    extension_seconds: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

class TransitSignalPriorityEngine:
    """Grant a short green extension to qualifying, imminent transit."""

    def evaluate_transit_priority(self, req: TransitPriorityRequest) -> TSPDecision:
        """Return a 15-second extension for qualifying arrivals within 20 seconds."""
        action = "NONE"
        extension = 0
        
        # Give absolute priority to BRT or high-occupancy transit arriving within 20 seconds
        if req.transit_type in ["BRT", "TRAM"] or req.passenger_count > 30:
            if req.estimated_arrival_seconds <= 20:
                action = "GREEN_EXTENDED"
                extension = 15

        return TSPDecision(
            request_id=f"TSP-{datetime.utcnow().strftime('%H%M%S')}-{req.vehicle_id}",
            intersection_id=req.intersection_id,
            action_taken=action,
            extension_seconds=extension
        )
