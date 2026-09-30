"""Core intersection identity and mutable signal-state entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class IntersectionID:
    """Strongly typed identifier used to avoid passing an unlabelled string."""

    value: str

@dataclass
class IntersectionState:
    """Current controller phase and its recent phase history."""

    intersection_id: IntersectionID
    current_phase: int
    active_green_duration_seconds: int
    is_emergency_preempted: bool
    phase_history: List[int] = field(default_factory=list)

    def validate_safety_bounds(self, min_green: int, max_green: int) -> bool:
        """Check whether the active green time falls inside inclusive bounds.

        Emergency preemption bypasses the duration check. The method reports
        validity only; it does not modify the state.
        """
        if self.is_emergency_preempted:
            return True
        if self.active_green_duration_seconds < min_green or self.active_green_duration_seconds > max_green:
            return False
        return True
