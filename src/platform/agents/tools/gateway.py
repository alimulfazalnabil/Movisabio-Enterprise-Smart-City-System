from pydantic import BaseModel
from typing import Dict, List, Any
from src.platform.agents.registry.agent import Agent, RiskClass

class ToolDefinition(BaseModel):
    tool_id: str
    risk_level: RiskClass
    required_permissions: List[str]

class ToolGateway:
    def __init__(self):
        self.registered_tools: Dict[str, ToolDefinition] = {}
        
    def register_tool(self, tool: ToolDefinition) -> None:
        self.registered_tools[tool.tool_id] = tool
        
    def evaluate_invocation(self, agent: Agent, tool_id: str) -> bool:
        """
        Tool Gateway zero-trust evaluation of a tool execution attempt.
        """
        tool = self.registered_tools.get(tool_id)
        if not tool:
            return False
            
        # 1. Is tool explicitly bound to agent?
        if tool_id not in agent.allowed_tools:
            return False
            
        # 2. Does agent have all permissions required by the tool?
        for perm in tool.required_permissions:
            if perm not in agent.permissions:
                return False
                
        # 3. Can the agent execute actions at this risk level?
        if not agent.can_execute_action(tool.risk_level):
            return False
            
        return True
