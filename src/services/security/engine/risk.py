from src.services.security.models.schemas import Threat, CyberPhysicalAsset

class RiskEngine:
    def calculate_risk(self, threat: Threat, asset: CyberPhysicalAsset) -> str:
        """
        Calculates cyber-physical risk score based on multiple dimensions.
        In this simplified model, we combine discrete severity ratings.
        """
        score = 0
        
        # Threat severity
        severity_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        score += severity_map.get(threat.severity, 1)
        
        # Asset criticality
        score += severity_map.get(asset.criticality, 1)
        
        # Threat exploitability
        score += severity_map.get(threat.exploitability, 1)
        
        # Exposure
        if asset.exposure == "INTERNET":
            score += 2
        elif asset.exposure == "INTERNAL":
            score += 1
            
        if score >= 12:
            return "CRITICAL"
        elif score >= 9:
            return "HIGH"
        elif score >= 6:
            return "MEDIUM"
        else:
            return "LOW"
