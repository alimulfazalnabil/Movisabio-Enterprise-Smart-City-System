"""Generate fixed-cycle signal plans with a Webster-style calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Dict, List, Optional
from aitcs.domain.value_objects import GranularTrafficState

@dataclass(frozen=True)
class OptimizedSignalPlan:
    """Cycle length, phase splits and clearance times for one intersection."""

    intersection_id: str
    optimal_cycle_length: int
    phase_splits: Dict[int, int]
    yellow_duration: int
    all_red_duration: int
    offset_seconds: int
    plan_type: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

class SignalOptimizationEngine:
    """Allocate green time from approach volumes and weather conditions."""

    def __init__(self, default_yellow: int = 4, default_all_red: int = 2, saturation_flow_rate: float = 1800.0):
        """Configure clearance times and saturation flow in vehicles per hour."""

        self.default_yellow = default_yellow
        self.default_all_red = default_all_red
        self.saturation_flow_rate = saturation_flow_rate

    def optimize_signal_plan(
        self,
        intersection_id: str,
        current_state: GranularTrafficState,
        approach_volumes: Dict[int, float],
        weather_condition: str = "CLEAR",
        current_time: Optional[time] = None
    ) -> OptimizedSignalPlan:
        """Calculate a cycle and per-phase green splits.

        Args:
            intersection_id: Intersection receiving the plan.
            current_state: Snapshot used to derive the progression offset.
            approach_volumes: Mapping of phase number to hourly volume.
            weather_condition: ``CLEAR``, ``RAIN``, ``SNOW`` or ``FOG``.
            current_time: Reserved for time-aware policies; defaults to now.

        Returns:
            A bounded signal plan. It is not safety-approved or transmitted.
        """
        if current_time is None: current_time = datetime.now().time()

        plan_type = "WEBSTER_OPTIMAL"
        lost_time = (self.default_yellow + self.default_all_red) * max(2, len(approach_volumes))
        weather_mult = 1.25 if weather_condition in ["RAIN", "SNOW", "FOG"] else 1.0
        if weather_mult > 1.0: plan_type = f"WEATHER_ADAPTIVE_{weather_condition}"

        flow_ratios, sum_y = {}, 0.0
        for phase, vol in approach_volumes.items():
            y_ratio = max(0.05, vol / self.saturation_flow_rate)
            flow_ratios[phase] = y_ratio
            sum_y += y_ratio
        sum_y = min(0.85, sum_y)

        webster_cycle = (1.5 * lost_time + 5.0) / (1.0 - sum_y)
        optimal_cycle = max(60, min(180, int(webster_cycle * weather_mult)))
        effective_cycle = optimal_cycle - lost_time

        phase_splits = {}
        for phase, y_ratio in flow_ratios.items():
            green = int(effective_cycle * (y_ratio / sum_y)) if sum_y > 0 else int(effective_cycle / len(approach_volumes))
            phase_splits[phase] = max(7, min(100, green))

        return OptimizedSignalPlan(
            intersection_id=intersection_id,
            optimal_cycle_length=optimal_cycle,
            phase_splits=phase_splits,
            yellow_duration=self.default_yellow,
            all_red_duration=self.default_all_red,
            offset_seconds=int(current_state.average_speed_kmh * 0.4),
            plan_type=plan_type,
            timestamp=datetime.utcnow()
        )
