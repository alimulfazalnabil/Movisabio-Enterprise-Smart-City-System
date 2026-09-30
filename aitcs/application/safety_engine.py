"""Apply hard timing bounds and phase-conflict rules to signal commands."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set, Optional

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
    timestamp: datetime = field(default_factory=datetime.utcnow)

class SafetyValidationEngine:
    """Independent rule-based gate between optimization and controllers."""

    def __init__(self, min_green: int = 7, max_green: int = 120, min_yellow: int = 4, min_all_red: int = 2, conflict_matrix: Optional[Dict[int, Set[int]]] = None):
        """Configure timing limits and conflicting phases.

        ``conflict_matrix`` maps each requested phase to phases that cannot be
        active at the same time.
        """

        self.min_green = min_green
        self.max_green = max_green
        self.min_yellow = min_yellow
        self.min_all_red = min_all_red
        self.conflict_matrix = conflict_matrix or {1: {3, 4}, 2: {3, 4}, 3: {1, 2}, 4: {1, 2}}

    def validate_and_sanitize(
        self,
        intersection_id: str,
        requested_phase: int,
        requested_green: int,
        requested_yellow: int,
        requested_all_red: int,
        active_conflicting_phases: Optional[Set[int]] = None,
        is_emergency: bool = False
    ) -> SanitizedSignalCommand:
        """Approve, clamp or replace a requested signal command.

        Args:
            intersection_id: Controller target.
            requested_phase: Phase proposed by an upstream engine.
            requested_green: Requested green duration in seconds.
            requested_yellow: Requested yellow duration in seconds.
            requested_all_red: Requested all-red duration in seconds.
            active_conflicting_phases: Phases currently active elsewhere.
            is_emergency: Enables the explicit preemption policy.

        Returns:
            A new command containing enforced durations and any override reason.
        """
        active_conflicts = active_conflicting_phases or set()
        
        if is_emergency:
            return SanitizedSignalCommand(
                intersection_id=intersection_id, approved_phase=requested_phase,
                green_duration_seconds=self.max_green, yellow_duration_seconds=self.min_yellow,
                all_red_duration_seconds=self.min_all_red, is_fallback_active=False,
                override_reason="Emergency vehicle preemption override active."
            )

        if self.conflict_matrix.get(requested_phase, set()).intersection(active_conflicts):
            return SanitizedSignalCommand(
                intersection_id=intersection_id, approved_phase=1,
                green_duration_seconds=self.min_green, yellow_duration_seconds=self.min_yellow,
                all_red_duration_seconds=self.min_all_red, is_fallback_active=True,
                override_reason="Conflict detected. Enforcing safe fallback."
            )

        approved_green = max(self.min_green, min(self.max_green, requested_green))
        return SanitizedSignalCommand(
            intersection_id=intersection_id, approved_phase=requested_phase,
            green_duration_seconds=approved_green, yellow_duration_seconds=max(self.min_yellow, requested_yellow),
            all_red_duration_seconds=max(self.min_all_red, requested_all_red),
            is_fallback_active=False, override_reason=None
        )
