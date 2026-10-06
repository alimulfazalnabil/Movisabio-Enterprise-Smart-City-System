from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class AppFunction(BaseModel):
    function_id: str
    application_id: str
    name: str
    event_trigger: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FunctionExecutor:
    def __init__(self):
        self.functions: Dict[str, AppFunction] = {}
        
    def register_function(self, function: AppFunction) -> AppFunction:
        self.functions[function.function_id] = function
        return function
        
    def execute_function(self, function_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if function_id not in self.functions:
            raise ValueError("Function not found")
        # In a real system, this would spin up a short-lived container or fire a lambda
        return {"status": "success", "executed_function": function_id, "payload_size": len(payload)}
