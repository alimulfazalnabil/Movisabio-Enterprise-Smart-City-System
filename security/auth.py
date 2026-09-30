from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from security.rbac import Role, Permission, has_permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock function to decode token and extract role (e.g. from JWT or Keycloak)
def get_current_user_role(token: str = Depends(oauth2_scheme)) -> Role:
    # In a real environment, decode JWT here
    # For now, return a default role for development
    if token == "test-token":
        return Role.TRAFFIC_ENGINEER
    return Role.VIEWER

def require_permission(permission: Permission):
    def permission_checker(role: Role = Depends(get_current_user_role)):
        if not has_permission(role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required permission: {permission}"
            )
        return role
    return permission_checker
