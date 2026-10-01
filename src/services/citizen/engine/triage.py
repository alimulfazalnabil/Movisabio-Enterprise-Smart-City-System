import math
from typing import List, Optional
from src.services.citizen.models.schemas import CitizenServiceRequest, ServiceCatalogEntry, RequestStatus

class RequestTriageEngine:
    """
    Handles duplicate detection, routing, and triage classification for citizen requests.
    """
    
    def calculate_distance(self, loc1: dict, loc2: dict) -> float:
        """Simple Euclidean distance approximation for testing."""
        return math.sqrt((loc1.get("lat", 0) - loc2.get("lat", 0))**2 + 
                         (loc1.get("lon", 0) - loc2.get("lon", 0))**2)
    
    def detect_duplicate(self, 
                        new_request: CitizenServiceRequest, 
                        existing_requests: List[CitizenServiceRequest], 
                        distance_threshold_deg: float = 0.001) -> Optional[str]:
        """
        Identifies if this request is a likely duplicate of an existing active request.
        """
        for req in existing_requests:
            if req.status in [RequestStatus.CLOSED, RequestStatus.RESOLVED, RequestStatus.REJECTED, RequestStatus.DISMISSED]:
                continue
                
            if req.category == new_request.category:
                dist = self.calculate_distance(new_request.location, req.location)
                if dist <= distance_threshold_deg:
                    return req.request_id
                    
        return None
        
    def route_request(self, request: CitizenServiceRequest, catalog: List[ServiceCatalogEntry]) -> CitizenServiceRequest:
        """
        Routes a request to the appropriate department based on the service catalog.
        """
        for entry in catalog:
            if entry.service_id == request.service_id:
                request.assigned_department = entry.department
                request.status = RequestStatus.TRIAGED
                return request
                
        request.assigned_department = "GENERAL_SUPPORT"
        request.status = RequestStatus.TRIAGED
        return request
