from typing import Dict, Any, Optional
from pydantic import BaseModel
import datetime

class SignalDecision(BaseModel):
    intersection_id: str
    desired_phase: str
    desired_state: str # e.g. GREEN
    reason: str

class OptimizationEngine:
    """
    Level 1 — Rule-based optimization.
    """
    def compute_decision(self, traffic_state: Any) -> SignalDecision:
        # Example logic: if queue is high, request GREEN
        return SignalDecision(
            intersection_id=traffic_state.intersection_id,
            desired_phase="North-South",
            desired_state="GREEN",
            reason="High queue pressure"
        )
