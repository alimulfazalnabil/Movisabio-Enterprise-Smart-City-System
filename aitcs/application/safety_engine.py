"""Rule-based safety boundary for signal commands.

This component is intentionally deterministic and independent from AI/model
logic. Emergency handling does not bypass timing bounds or phase validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional, Set


@dataclass(frozen=True)
class SanitizedSignalCommand:
    """Signal command approved or replaced by the safety boundary."""

    intersection_id: str
    approved_phase: int
    green_duration_seconds: int
    yellow_duration_seconds: int
    all_red_duration_seconds: int
    is_fallback_active: bool
    override_reason: Optional[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SafetyValidationEngine:
    """Independent hard gate between optimization and controller adapters."""

    def __init__(
        self,
        min_green: int = 7,
        max_green: int = 120,
        min_yellow: int = 4,
        min_all_red: int = 2,
        conflict_matrix: Optional[Dict[int, Set[int]]] = None,
    ):
        if min_green <= 0 or max_green < min_green:
            raise ValueError("Invalid green timing bounds")
        if min_yellow <= 0 or min_all_red <= 0:
            raise ValueError("Clearance intervals must be positive")

        self.min_green = min_green
        self.max_green = max_green
        self.min_yellow = min_yellow
        self.min_all_red = min_all_red
        self.conflict_matrix = conflict_matrix or {
            1: {3, 4},
            2: {3, 4},
            3: {1, 2},
            4: {1, 2},
        }

    def validate_and_sanitize(
        self,
        intersection_id: str,
        requested_phase: int,
        requested_green: int,
        requested_yellow: int,
        requested_all_red: int,
        active_conflicting_phases: Optional[Set[int]] = None,
        is_emergency: bool = False,
    ) -> SanitizedSignalCommand:
        """Validate, clamp, or fail-safe a candidate signal command.

        Emergency mode is an explicit priority annotation; it does not disable
        conflict checks, timing bounds, or input validation.
        """
        if not intersection_id:
            raise ValueError("intersection_id is required")
        if requested_phase not in self.conflict_matrix:
            return self._fallback(intersection_id, "Unknown signal phase")
        if requested_green <= 0 or requested_yellow <= 0 or requested_all_red <= 0:
            return self._fallback(intersection_id, "Non-positive timing requested")

        active_conflicts = active_conflicting_phases or set()
        if self.conflict_matrix[requested_phase].intersection(active_conflicts):
            return self._fallback(intersection_id, "Conflict detected")

        approved_green = max(self.min_green, min(self.max_green, int(requested_green)))
        approved_yellow = max(self.min_yellow, int(requested_yellow))
        approved_all_red = max(self.min_all_red, int(requested_all_red))

        return SanitizedSignalCommand(
            intersection_id=intersection_id,
            approved_phase=requested_phase,
            green_duration_seconds=approved_green,
            yellow_duration_seconds=approved_yellow,
            all_red_duration_seconds=approved_all_red,
            is_fallback_active=False,
            override_reason=(
                "Emergency priority policy active; bounded command approved."
                if is_emergency
                else None
            ),
        )

    def _fallback(self, intersection_id: str, reason: str) -> SanitizedSignalCommand:
        return SanitizedSignalCommand(
            intersection_id=intersection_id,
            approved_phase=1,
            green_duration_seconds=self.min_green,
            yellow_duration_seconds=self.min_yellow,
            all_red_duration_seconds=self.min_all_red,
            is_fallback_active=True,
            override_reason=reason,
        )
