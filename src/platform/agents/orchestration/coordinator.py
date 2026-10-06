from pydantic import BaseModel
from typing import Dict, List, Optional
from src.platform.agents.registry.agent import Agent

class AgentMessage(BaseModel):
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: str
    payload: Dict[str, str]
    confidence: float

class Coordinator:
    def __init__(self):
        self.message_bus: List[AgentMessage] = []
        
    def route_message(self, message: AgentMessage) -> None:
        """
        Routes structured messages between agents.
        """
        self.message_bus.append(message)
        
    def resolve_conflict(self, proposals: List[Dict]) -> Optional[Dict]:
        """
        Resolves conflicts by priority hierarchy (e.g. Safety/Emergency > Public Transit > Normal Traffic).
        """
        if not proposals:
            return None
            
        # Simplified priority logic
        priority_map = {
            "emergency_agent": 100,
            "transit_agent": 50,
            "traffic_agent": 10
        }
        
        proposals.sort(key=lambda p: priority_map.get(p.get("agent_id", ""), 0), reverse=True)
        return proposals[0] # Win based on priority
