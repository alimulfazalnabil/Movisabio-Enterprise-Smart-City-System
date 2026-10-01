from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from src.auth.jwt import validate_access_token, AuthenticationException
from src.core.exceptions import PermissionDeniedException
from src.core.context import set_tenant_context, set_user_context
from src.auth.authorization import AuthorizationService
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
    
    return payload

def require_permission(action: str):
    """
    Dependency generator enforcing RBAC via AuthorizationService.
    Usage: @router.get("/traffic", dependencies=[Depends(require_permission("traffic.read"))])
    """
    async def permission_checker(payload: dict = Depends(get_current_token_payload)):
        tenant_id = payload.get("tenant_id")
        
        # We pass the payload as the subject. The AuthorizationService handles role mapping.
        AuthorizationService.authorize(
            subject=payload,
            action=action,
            tenant=tenant_id
        )
        return payload
        
    return permission_checker
