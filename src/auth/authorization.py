from src.core.exceptions import PermissionDeniedException, TenantIsolationException
from typing import Optional, List, Dict, Any
from src.auth.permissions import Permission, ROLE_PERMISSIONS
import logging

logger = logging.getLogger("movisabio.security")

class AuthorizationService:
    """
    Core Authorization Engine decoupling RBAC/Policy decisions from application endpoints.
    """
    
    @staticmethod
    def authorize(
        subject: dict, 
        action: str, 
        tenant: str, 
        resource: Optional[Any] = None,
        scope: Optional[List[str]] = None
    ) -> bool:
        """
        Evaluates the full authorization pipeline.
        Raises PermissionDeniedException or TenantIsolationException on DENY.
        Returns True on ALLOW.
        """
        user_id = subject.get("sub")
        subject_tenant = subject.get("tenant_id")
        roles = subject.get("roles", ["Viewer"])
        
        # 1. Tenant Isolation Check
        if subject_tenant != tenant:
            logger.warning(f"Cross-tenant access attempt: User {user_id} (Tenant {subject_tenant}) -> Target Tenant {tenant}")
            raise TenantIsolationException("Cross-tenant access is strictly forbidden.")
            
        # 2. Compile Permissions
        user_permissions = set()
        for role in roles:
            if role in ROLE_PERMISSIONS:
                user_permissions.update(ROLE_PERMISSIONS[role])
        
        # Add any explicitly granted custom permissions from token/DB
        custom_perms = subject.get("permissions", [])
        user_permissions.update(custom_perms)
        
        # 3. RBAC Check
        if action not in user_permissions:
            logger.warning(f"Permission denied: User {user_id} lacks {action}")
            raise PermissionDeniedException(f"Missing required permission: {action}")
            
        # 4. Resource Scope Check (if a resource or scope is provided)
        # e.g., if scope restricts access to ["INT-001", "INT-002"], ensure resource.id is in scope
        if resource and hasattr(resource, "id") and scope is not None:
            if resource.id not in scope:
                logger.warning(f"Scope denied: User {user_id} has no access to resource {resource.id}")
                raise PermissionDeniedException(f"Resource {resource.id} is outside permitted scope.")
                
        # 5. Traffic Control Safety & Audit Boundary Check
        if action in [Permission.TRAFFIC_CONTROL, Permission.TRAFFIC_OVERRIDE, Permission.DEVICE_COMMAND]:
            logger.info(
                f"Privileged infrastructure command authorized", 
                extra={
                    "user_id": user_id,
                    "action": action,
                    "tenant_id": tenant,
                    "resource_id": resource.id if resource else None,
                    "policy_version": "1.0"
                }
            )
            
        return True
