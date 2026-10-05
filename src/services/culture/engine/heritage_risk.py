from src.services.culture.models.schemas import HeritageRiskIndicator

class HeritageRiskEngine:
    def calculate_risk(self, asset_id: str, hazard: float, exposure: float, vulnerability: float) -> HeritageRiskIndicator:
        """
        Calculates the risk score for a heritage asset based on hazard, exposure, and vulnerability.
        """
        risk_score = hazard * exposure * vulnerability
        return HeritageRiskIndicator(
            asset_id=asset_id,
            hazard=hazard,
            exposure=exposure,
            vulnerability=vulnerability,
            risk_score=risk_score
        )
