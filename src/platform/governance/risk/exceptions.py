from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class ExceptionStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class ArchitectureException(BaseModel):
    exception_id: str
    requester: str
    standard_violated: str
    reason: str
    mitigation: str
    status: ExceptionStatus = ExceptionStatus.REQUESTED
    expiration_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ExceptionEngine:
    def __init__(self):
        self.exceptions: Dict[str, ArchitectureException] = {}
        
    def request_exception(self, exception: ArchitectureException) -> ArchitectureException:
        self.exceptions[exception.exception_id] = exception
        return exception
        
    def review_exception(self, exception_id: str, new_status: ExceptionStatus, expiration: Optional[datetime] = None) -> ArchitectureException:
        if exception_id not in self.exceptions:
            raise ValueError("Exception not found")
        exc = self.exceptions[exception_id]
        exc.status = new_status
        if expiration:
            exc.expiration_date = expiration
        return exc
