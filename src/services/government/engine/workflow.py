from src.services.government.models.schemas import GovernmentCase
from datetime import datetime

class WorkflowEngine:
    def transition_case(self, case: GovernmentCase, action: str) -> GovernmentCase:
        """
        Transitions a government case through its lifecycle workflow.
        """
        valid_transitions = {
            "SUBMITTED": {"start_review": "UNDER_REVIEW", "close": "CLOSED"},
            "UNDER_REVIEW": {"approve": "APPROVED", "reject": "REJECTED"},
            "APPROVED": {"close": "CLOSED"},
            "REJECTED": {"close": "CLOSED"},
        }
        
        current_status = case.status
        if current_status in valid_transitions and action in valid_transitions[current_status]:
            case.status = valid_transitions[current_status][action]
            
        return case
