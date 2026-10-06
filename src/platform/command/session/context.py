from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class CommandContext(BaseModel):
    user_id: str
    organization_id: str
    tenant_id: str
    role: str
    permissions: List[str]
    active_situation: Optional[str] = None
    
class ContextEngine:
    def __init__(self):
        self.sessions: Dict[str, CommandContext] = {}
        
    def create_session(self, session_id: str, context: CommandContext) -> CommandContext:
        self.sessions[session_id] = context
        return context
        
    def authorize_action(self, session_id: str, required_permission: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        return required_permission in session.permissions
