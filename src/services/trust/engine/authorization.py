from src.services.trust.models.schemas import AccessRequest, Identity, DataAsset, TrustDecision

class AuthorizationEngine:
    def evaluate_access(self, request: AccessRequest, identity: Identity, asset: DataAsset) -> TrustDecision:
        """
        Evaluates an access request against the identity and asset classifications.
        """
        if identity.status not in ["VERIFIED", "ACTIVE"]:
            return TrustDecision(decision="DENY", reason="Identity not active or verified")
            
        if asset.classification in ["CONFIDENTIAL", "PERSONAL"]:
            if request.purpose not in ["AUTHORIZED_PROCESSING", "EXPLICIT_CONSENT"]:
                return TrustDecision(decision="DENY", reason="Purpose not authorized for sensitive data")
                
        return TrustDecision(decision="ALLOW", reason="Authorized by default rule")
