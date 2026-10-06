from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class GlobalServiceStatus(BaseModel):
    service_id: str
    region_id: str
    tenant_id: str
    version: str
    health_status: str
    last_reported: datetime = Field(default_factory=datetime.utcnow)

class GlobalServiceCatalog:
    def __init__(self):
        self.services: Dict[str, GlobalServiceStatus] = {}
        
    def register_regional_service(self, service: GlobalServiceStatus) -> GlobalServiceStatus:
        key = f"{service.region_id}::{service.service_id}::{service.tenant_id}"
        self.services[key] = service
        return service
        
    def query_global_health(self, service_id: str) -> Dict[str, str]:
        health_report = {}
        for key, service in self.services.items():
            if service.service_id == service_id:
                health_report[service.region_id] = service.health_status
        return health_report
