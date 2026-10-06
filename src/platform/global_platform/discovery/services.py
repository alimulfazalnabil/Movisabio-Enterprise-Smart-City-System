from pydantic import BaseModel
from typing import Dict, List, Optional

class ServiceEndpoint(BaseModel):
    service_name: str
    region_id: str
    endpoint: str
    health: str = "HEALTHY"
    
class GlobalServiceRegistry:
    def __init__(self):
        self.endpoints: List[ServiceEndpoint] = []
        
    def register(self, endpoint: ServiceEndpoint) -> None:
        self.endpoints.append(endpoint)
        
    def route_request(self, service_name: str, requested_region: str) -> Optional[str]:
        """
        Naive routing: Route to the requested region if healthy.
        Otherwise, fail (preventing accidental cross-region data transfer).
        """
        for ep in self.endpoints:
            if ep.service_name == service_name and ep.region_id == requested_region and ep.health == "HEALTHY":
                return ep.endpoint
        return None
