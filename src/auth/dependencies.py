from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from src.auth.jwt import validate_access_token, AuthenticationException
from src.core.exceptions import PermissionDeniedException
from src.core.context import set_tenant_context, set_user_context
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

async def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Extracts, validates, and sets the context for the current request.
    """
    payload = validate_access_token(token)
    
    # Establish Tenant and User Context
    set_tenant_context(payload.get("tenant_id"))
    set_user_context(payload.get("sub"))
    
    # In a real system, we might publish an audit event here, but typically we 
    # log it via middleware or at the endpoint boundary.
    return payload

def require_permission(permission: str):
    """
    Dependency generator enforcing RBAC.
    Usage: @router.get("/traffic", dependencies=[Depends(require_permission("traffic.read"))])
    """
    async def permission_checker(payload: dict = Depends(get_current_token_payload)):
        # Extract permissions from token or fetch from DB cache based on payload['roles']
        # For simplicity in this architectural phase, we assume the token contains a 'permissions' array
        # or we would query the RBAC engine here.
        user_permissions = payload.get("permissions", [])
        
        # Traffic Control Boundary Specific Log
        if permission in ["traffic.control", "traffic.override"]:
            logging.getLogger("movisabio").info(
                f"High-privilege access check", 
                extra={
                    "user_id": payload.get("sub"),
                    "tenant_id": payload.get("tenant_id"),
                    "requested_permission": permission
                }
            )

        if permission not in user_permissions:
            raise PermissionDeniedException(f"Missing required permission: {permission}")
            
        return payload
        
    return permission_checker
