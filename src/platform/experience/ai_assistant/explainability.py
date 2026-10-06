from pydantic import BaseModel
from typing import Dict, List

class ExplainableRecommendation(BaseModel):
    recommendation_id: str
    problem_statement: str
    action_recommended: str
    confidence_score: float
    evidence_sources: List[str]
    safety_status: str
    policy_reference: str
    
class Assistant:
    def format_explanation(self, rec: ExplainableRecommendation) -> str:
        """Formats an AI recommendation into a structured explanation, avoiding 'hallucinated reasoning'."""
        lines = [
            f"RECOMMENDATION: {rec.action_recommended}",
            f"PROBLEM: {rec.problem_statement}",
            f"EVIDENCE: {', '.join(rec.evidence_sources)}",
            f"CONFIDENCE: {rec.confidence_score:.2f}",
            f"SAFETY: {rec.safety_status}",
            f"POLICY: {rec.policy_reference}"
        ]
        return "\n".join(lines)
