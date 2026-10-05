from src.services.resilience.models.schemas import HazardEvent, ExposureEntity, RiskAssessment
import uuid

class RiskAssessmentEngine:
    def evaluate_risk(self, hazard: HazardEvent, entity: ExposureEntity) -> RiskAssessment:
        """
        Evaluates risk based on hazard intensity, vulnerability, and criticality.
        Risk = f(Hazard, Exposure, Vulnerability, Capacity)
        """
        # Criticality multiplier
        crit_map = {"C0": 0.5, "C1": 1.0, "C2": 1.5, "C3": 2.0, "C4": 3.0}
        crit_factor = crit_map.get(entity.criticality, 1.0)
        
        # Risk Score Calculation
        score = hazard.intensity * entity.vulnerability_score * crit_factor
        
        # Determine Level
        risk_level = "NORMAL"
        if score >= 2.0:
            risk_level = "CRITICAL"
        elif score >= 1.5:
            risk_level = "VERY_HIGH"
        elif score >= 1.0:
            risk_level = "HIGH"
        elif score >= 0.5:
            risk_level = "ELEVATED"
        elif score >= 0.1:
            risk_level = "WATCH"
            
        return RiskAssessment(
            assessment_id=str(uuid.uuid4()),
            hazard_id=hazard.hazard_id,
            entity_id=entity.entity_id,
            risk_level=risk_level,
            compound_score=score
        )
