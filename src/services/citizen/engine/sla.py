from datetime import datetime, timedelta, timezone
from typing import List, Optional
from src.services.citizen.models.schemas import CitizenServiceRequest, ServiceCatalogEntry

class SLAEngine:
    """
    Computes SLA targets and evaluates compliance.
    """
    
    def apply_sla(self, request: CitizenServiceRequest, catalog: List[ServiceCatalogEntry]) -> CitizenServiceRequest:
        """
        Calculates and applies the SLA deadline based on the service catalog.
        """
        for entry in catalog:
            if entry.service_id == request.service_id:
                request.sla_due_at = request.created_at + timedelta(hours=entry.sla_target_hours)
                return request
                
        # Default SLA if service not found
        request.sla_due_at = request.created_at + timedelta(hours=72)
        return request
        
    def check_sla_breach(self, request: CitizenServiceRequest) -> bool:
        """
        Returns True if the request is currently breaching its SLA.
        """
        if not request.sla_due_at:
            return False
            
        if request.status in ["RESOLVED", "CLOSED", "CITIZEN_REVIEW", "REJECTED", "DUPLICATE", "DISMISSED"]:
            return False
            
        now = datetime.now(timezone.utc)
        return now > request.sla_due_at
