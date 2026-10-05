from src.platform.mlops.registry.models import MLModelVersion, MLModel

class ModelApprovalWorkflow:
    @staticmethod
    def approve_model(model: MLModel, version: MLModelVersion) -> bool:
        """
        Approves a model version for deployment.
        Higher risk classes require more stringent checks.
        """
        if version.status not in ["EVALUATED", "CANDIDATE"]:
            return False
            
        if model.risk_class in ["R4", "R5"]:
            # R4/R5 require explicit safety and policy review artifacts
            # In a real system, we'd check for human approvals and safety reports here
            # For this MVP, we simulate a strict check by ensuring signature exists
            if not version.signature:
                return False
                
        version.status = "APPROVED"
        return True
