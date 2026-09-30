from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    timestamp: str

class MoviSabioException(Exception):
    """Base exception for MoviSabio Enterprise Platform"""
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

class TrafficControllerUnavailableException(MoviSabioException):
    def __init__(self, message: str = "Traffic controller is currently unavailable."):
        super().__init__("TRAFFIC_CONTROLLER_UNAVAILABLE", message, 503)

class PermissionDeniedException(MoviSabioException):
    def __init__(self, message: str = "Permission denied for this resource."):
        super().__init__("PERMISSION_DENIED", message, 403)

class TenantIsolationException(MoviSabioException):
    def __init__(self, message: str = "Cross-tenant access is forbidden."):
        super().__init__("CROSS_TENANT_ACCESS_FORBIDDEN", message, 403)

async def movisabio_exception_handler(request: Request, exc: MoviSabioException):
    import datetime
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                # In production, request_id comes from OpenTelemetry/middleware
                "request_id": getattr(request.state, "request_id", "req_unknown"),
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
        }
    )
