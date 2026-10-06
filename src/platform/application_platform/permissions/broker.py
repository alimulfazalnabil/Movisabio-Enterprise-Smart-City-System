from typing import List, Dict, Set

class PermissionBroker:
    def __init__(self):
        self.app_permissions: Dict[str, Set[str]] = {}
        # Restricted scopes that require exceptional governance
        self.restricted_scopes: Set[str] = {"traffic.control", "device.write", "controller.write"}
        
    def grant_permissions(self, application_id: str, permissions: List[str]) -> bool:
        """
        Grants permissions to an app. Returns False if requested permissions contain restricted scopes.
        """
        requested = set(permissions)
        if not requested.isdisjoint(self.restricted_scopes):
            return False
            
        if application_id not in self.app_permissions:
            self.app_permissions[application_id] = set()
        self.app_permissions[application_id].update(requested)
        return True
        
    def check_permission(self, application_id: str, permission: str) -> bool:
        return permission in self.app_permissions.get(application_id, set())
