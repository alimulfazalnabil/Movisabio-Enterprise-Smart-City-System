from src.services.trust.models.schemas import DataTransferRequest, TrustDecision
from typing import Dict, List

class ResidencyEngine:
    def __init__(self, allowed_transfers: Dict[str, List[str]]):
        # Maps source jurisdiction to a list of allowed target jurisdictions
        self.allowed_transfers = allowed_transfers
        
    def evaluate_transfer(self, request: DataTransferRequest) -> TrustDecision:
        """
        Evaluates a data transfer request based on residency rules.
        """
        if request.source_jurisdiction == request.target_jurisdiction:
            return TrustDecision(decision="ALLOW", reason="Domestic transfer")
            
        allowed_targets = self.allowed_transfers.get(request.source_jurisdiction, [])
        if request.target_jurisdiction in allowed_targets:
            return TrustDecision(decision="ALLOW", reason="Cross-border transfer permitted by policy")
            
        return TrustDecision(decision="DENY", reason="Cross-border transfer prohibited by residency rules")
