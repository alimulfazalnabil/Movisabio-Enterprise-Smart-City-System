"""Turn current and predicted traffic demand into a signal-phase proposal."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from aitcs.domain.value_objects import GranularTrafficState
from aitcs.application.prediction_engine import PredictionResult

@dataclass(frozen=True)
class SignalDecision:
    """Proposed phase timing before independent safety validation."""

    intersection_id: str
    selected_phase: int
    green_duration_seconds: int
    yellow_duration_seconds: int
    all_red_duration_seconds: int
    phase_skipped: bool
    cycle_length_seconds: int
    offset_seconds: int
    decision_reason: str
    confidence_score: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class AIDecisionEngine:
    """Produce bounded adaptive timings from traffic pressure and arrivals."""

    def __init__(self, min_green: int = 7, max_green: int = 120, yellow_duration: int = 4, all_red: int = 2):
        """Configure green bounds and fixed clearance intervals in seconds."""

        self.min_green = min_green
        self.max_green = max_green
        self.yellow_duration = yellow_duration
        self.all_red = all_red

    def compute_signal_decision(
        self,
        intersection_id: str,
        current_state: GranularTrafficState,
        predictions: List[PredictionResult],
        current_phase: int = 1
    ) -> SignalDecision:
        """Build a timing proposal for the current intersection phase.

        Args:
            intersection_id: Intersection receiving the proposal.
            current_state: Latest normalized traffic snapshot.
            predictions: Forecasts; the one-minute horizon is preferred.
            current_phase: Controller phase currently active.

        Returns:
            A proposal that must still pass ``SafetyValidationEngine`` before
            being sent to a physical controller.
        """
        immediate_prediction = next((p for p in predictions if p.horizon_minutes == 1), None)
        predicted_queue = immediate_prediction.predicted_queue_length_meters if immediate_prediction else current_state.queue_length_meters
        predicted_arrivals = immediate_prediction.predicted_arrival_count if immediate_prediction else current_state.vehicle_count

        if current_state.vehicle_count == 0 and predicted_queue < 2.0:
            return SignalDecision(
                intersection_id=intersection_id,
                selected_phase=(current_phase % 4) + 1,
                green_duration_seconds=self.min_green,
                yellow_duration_seconds=self.yellow_duration,
                all_red_duration_seconds=self.all_red,
                phase_skipped=True,
                cycle_length_seconds=60,
                offset_seconds=0,
                decision_reason="Phase skipped due to zero detected vehicle demand.",
                confidence_score=0.98
            )

        pressure_factor = current_state.intersection_pressure / 100.0
        arrival_factor = predicted_arrivals / 50.0
        calculated_green = int(30.0 + (pressure_factor * 25.0) + (arrival_factor * 15.0))
        green_duration = max(self.min_green, min(self.max_green, calculated_green))
        cycle_length = max(60, green_duration * 2 + self.yellow_duration * 2 + self.all_red * 2)

        return SignalDecision(
            intersection_id=intersection_id,
            selected_phase=current_phase,
            green_duration_seconds=green_duration,
            yellow_duration_seconds=self.yellow_duration,
            all_red_duration_seconds=self.all_red,
            phase_skipped=False,
            cycle_length_seconds=cycle_length,
            offset_seconds=int(current_state.average_speed_kmh * 0.5),
            decision_reason="Normal adaptive split allocation.",
            confidence_score=immediate_prediction.confidence_score if immediate_prediction else 0.85
        )
