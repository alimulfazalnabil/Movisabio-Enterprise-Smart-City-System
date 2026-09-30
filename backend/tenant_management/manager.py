from typing import Dict, Any

class TenantManager:
    """
    Core SaaS module resolving multi-city multi-tenancy.
    Isolates data, configurations, and API keys between cities (e.g. Campinas vs Montevideo).
    """
    def __init__(self):
        self.active_tenants = {}
        
    def onboard_city(self, tenant_id: str, config: Dict[str, Any]):
        """
        Registers a new city to the MoviSabio SaaS platform.
        """
        self.active_tenants[tenant_id] = {
            "config": config,
            "status": "PROVISIONING",
            "features": config.get("subscription_tier", "STARTER")
        }
        return {"status": "SUCCESS", "message": f"City {tenant_id} onboarded."}
        
    def get_tenant_config(self, tenant_id: str):
        if tenant_id not in self.active_tenants:
            raise PermissionError(f"Tenant {tenant_id} not found or unauthorized.")
        return self.active_tenants[tenant_id]
