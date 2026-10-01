from datetime import datetime, timezone
from src.services.infrastructure.models.schemas import AssetCondition, FailureRisk, ConditionClass

class PredictiveMaintenanceEngine:
    """
    Evaluates asset condition and calculates failure risk to prioritize maintenance.
    """
    
    def calculate_failure_risk(self, condition: AssetCondition, age_years: float, expected_life_years: float) -> FailureRisk:
        probability = 0.0
        risk_level = "LOW"
        severity = "MEDIUM"
        evidence = []
        
        # Age-based degradation
        life_ratio = age_years / expected_life_years if expected_life_years > 0 else 1.0
        if life_ratio > 0.9:
            probability += 0.3
            evidence.append("near_end_of_life")
            
        # Condition-based degradation
        if condition.condition_class == ConditionClass.POOR:
            probability += 0.4
            evidence.append("poor_condition")
            risk_level = "ELEVATED"
        elif condition.condition_class == ConditionClass.CRITICAL:
            probability += 0.7
            evidence.append("critical_condition")
            risk_level = "HIGH"
            severity = "HIGH"
            
        probability = min(0.99, probability)
        if probability > 0.6:
            risk_level = "HIGH"
            severity = "HIGH"
            
        return FailureRisk(
            asset_id=condition.asset_id,
            failure_mode="GENERAL_DEGRADATION",
            probability=probability,
            severity=severity,
            risk_level=risk_level,
            prediction_window="30d",
            evidence=evidence,
            confidence=condition.confidence,
            model_version="risk-v1"
        )
