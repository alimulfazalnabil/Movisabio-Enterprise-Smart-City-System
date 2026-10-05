from src.services.food.models.schemas import FoodSecurityRisk

class FoodSecurityEngine:
    def calculate_territory_risk(self, availability: float, access: float, utilization: float, stability: float, territory_id: str) -> FoodSecurityRisk:
        """
        Calculates food security risk based on the 4 pillars of food security.
        """
        # Composite score calculation (simplified average)
        composite = (availability + access + utilization + stability) / 4.0
        
        risk_level = "LOW"
        if composite < 0.4:
            risk_level = "CRITICAL"
        elif composite < 0.6:
            risk_level = "HIGH"
        elif composite < 0.8:
            risk_level = "MODERATE"
            
        return FoodSecurityRisk(
            territory_id=territory_id,
            availability_score=availability,
            access_score=access,
            utilization_score=utilization,
            stability_score=stability,
            risk_level=risk_level
        )
