"""HTTP adapters for pedestrian timing and heuristic XAI explanations."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from aitcs.application.pedestrian_intelligence_engine import PedestrianIntelligenceEngine
from aitcs.application.mlops_xai_engine import MLOpsXAIEngine

router = APIRouter(prefix="/api/v1/intelligence", tags=["Pedestrian Intelligence & MLOps XAI"])

ped_engine = PedestrianIntelligenceEngine()
xai_engine = MLOpsXAIEngine()

class PedestrianPayload(BaseModel):
    """Observed pedestrian demand for one intersection."""

    intersection_id: str
    waiting_count: int
    elderly_count: int = 0
    school_mode: bool = False

class XAIPayload(BaseModel):
    """Decision metadata and numeric features to normalize for explanation."""

    decision_id: str
    model_version: str
    features: Dict[str, float]

@router.post("/pedestrian/optimize")
async def optimize_pedestrian_signal(payload: PedestrianPayload):
    """Return a rule-based pedestrian crossing-time recommendation."""
    result = ped_engine.calculate_crossing_timing(
        payload.intersection_id,
        payload.waiting_count,
        payload.elderly_count,
        payload.school_mode
    )
    return {"status": "success", "pedestrian_timing": result}

@router.post("/mlops/explain")
async def explain_ai_decision(payload: XAIPayload):
    """Return heuristic feature importance and drift metadata."""
    explanation = xai_engine.explain_decision(
        payload.decision_id,
        payload.model_version,
        payload.features
    )
    return {"status": "success", "explanation": explanation}
