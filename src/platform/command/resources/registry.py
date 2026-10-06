from pydantic import BaseModel
from typing import Dict, Any, Optional
import enum

class ResourceStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ACTIVE = "ACTIVE"
    UNAVAILABLE = "UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"

class Resource(BaseModel):
    resource_id: str
    organization_id: str
    type: str
    status: ResourceStatus = ResourceStatus.AVAILABLE
    current_task_id: Optional[str] = None
    
class ResourceRegistry:
    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        
    def register_resource(self, resource: Resource) -> Resource:
        self.resources[resource.resource_id] = resource
        return resource
        
    def allocate_resource(self, resource_id: str, task_id: str) -> Resource:
        if resource_id not in self.resources:
            raise ValueError("Resource not found")
            
        resource = self.resources[resource_id]
        if resource.status != ResourceStatus.AVAILABLE:
            raise ValueError(f"Resource {resource_id} is not available")
            
        resource.status = ResourceStatus.ASSIGNED
        resource.current_task_id = task_id
        return resource
