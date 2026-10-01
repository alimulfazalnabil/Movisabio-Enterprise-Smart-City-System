from contextvars import ContextVar
from typing import Optional

# These context variables track the identity and tenancy of the current request.
# They are safely isolated per-request in FastAPI (asyncio).

current_user_id: ContextVar[Optional[str]] = ContextVar("current_user_id", default=None)
current_tenant_id: ContextVar[Optional[str]] = ContextVar("current_tenant_id", default=None)
current_request_id: ContextVar[Optional[str]] = ContextVar("current_request_id", default=None)
current_correlation_id: ContextVar[Optional[str]] = ContextVar("current_correlation_id", default=None)

def set_tenant_context(tenant_id: str):
    """Sets the tenant context for the current execution flow."""
    current_tenant_id.set(tenant_id)

def get_tenant_context() -> Optional[str]:
    """Retrieves the current tenant context. Crucial for RLS / isolated queries."""
    return current_tenant_id.get()

def set_user_context(user_id: str):
    current_user_id.set(user_id)

def get_user_context() -> Optional[str]:
    return current_user_id.get()

def set_trace_context(request_id: str, correlation_id: str):
    current_request_id.set(request_id)
    current_correlation_id.set(correlation_id)

def get_trace_context() -> dict:
    return {
        "request_id": current_request_id.get(),
        "correlation_id": current_correlation_id.get()
    }
