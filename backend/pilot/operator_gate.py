from typing import Dict, Any

class OperatorApprovalGate:
    """
    Human-in-the-loop approval interface for Shadow Pilot phase transitions.
    """
    def __init__(self):
        self.pending_actions = {}
        
    def submit_for_approval(self, audit_entry: Dict) -> str:
        """
        AI submits a safe command. It stops here until human intervention.
        """
        request_id = audit_entry["audit_id"]
        self.pending_actions[request_id] = {
            "entry": audit_entry,
            "status": "PENDING_OPERATOR"
        }
        return request_id
        
    def review_action(self, request_id: str, approved: bool, operator_id: str) -> bool:
        """
        Human operator explicitly clicks "APPROVE" or "REJECT".
        """
        if request_id not in self.pending_actions:
            raise ValueError("Unknown request ID")
            
        self.pending_actions[request_id]["status"] = "APPROVED" if approved else "REJECTED"
        self.pending_actions[request_id]["operator"] = operator_id
        
        return approved
