from enum import Enum
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel

class RequestStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    RECEIVED = "RECEIVED"
    TRIAGED = "TRIAGED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_INFORMATION = "WAITING_FOR_INFORMATION"
    RESOLVED = "RESOLVED"
    CITIZEN_REVIEW = "CITIZEN_REVIEW"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"
    DUPLICATE = "DUPLICATE"
    DISMISSED = "DISMISSED"

class ServiceCatalogEntry(BaseModel):
    service_id: str
    name: str
    description: str
    department: str
    category: str
    eligibility: str
    required_information: List[str]
    optional_information: List[str]
    sla_target_hours: float
    priority_rules: dict
    workflow: str
    status_visibility: str
    enabled: bool = True

class CitizenServiceRequest(BaseModel):
    request_id: str
    tenant_id: str
    citizen_id: str
    service_id: str
    
    category: str
    subcategory: str
    title: str
    description: str
    
    location: dict
    geometry: dict
    address: str
    
    created_at: datetime
    updated_at: datetime
    
    priority: str = "P3"
    status: RequestStatus = RequestStatus.SUBMITTED
    assigned_department: Optional[str] = None
    assigned_operator: Optional[str] = None
    
    sla_due_at: Optional[datetime] = None
    
    verification_status: str = "PENDING"
    resolution_status: Optional[str] = None
    
    closed_at: Optional[datetime] = None
    parent_event_id: Optional[str] = None # For duplicates/correlation

class CitizenFeedback(BaseModel):
    feedback_id: str
    request_id: str
    citizen_id: str
    resolved: bool
    rating: Optional[int] = None
    comment: Optional[str] = None
    timestamp: datetime
