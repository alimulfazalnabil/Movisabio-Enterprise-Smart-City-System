from datetime import datetime, timezone
from typing import Optional
from src.services.priority.models.schemas import PriorityRequest, PriorityStatus, PriorityClass

class PriorityEligibilityEngine:
    """
    Evaluates whether a vehicle is legitimately eligible for priority 
    before it enters the arbitration pool.
    """
    
    def evaluate(self, request: PriorityRequest, vehicle_registry: dict) -> bool:
        """
        vehicle_registry is a mocked external source of authorized vehicles.
        """
        # 1. Freshness check
        if datetime.now(timezone.utc) > request.expires_at:
            request.status = PriorityStatus.EXPIRED
            return False
            
        # 2. Identity and Authorization check
        vehicle_data = vehicle_registry.get(request.vehicle_id)
        if not vehicle_data or not vehicle_data.get('authorized', False):
            request.status = PriorityStatus.REJECTED
            return False
            
        # 3. Confidence threshold
        if request.confidence < 0.85:
            request.status = PriorityStatus.REJECTED
            return False
            
        # 4. Class Validation
        authorized_class = vehicle_data.get('max_priority_class')
        if authorized_class:
            # Simple string comparison works here due to Enum structure (P0 < P1)
            if request.priority_class.value < authorized_class:
                request.status = PriorityStatus.REJECTED
                return False
                
        request.status = PriorityStatus.AUTHORIZED
        return True
