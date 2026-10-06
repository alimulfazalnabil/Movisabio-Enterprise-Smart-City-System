from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class InstallationState(str, enum.Enum):
    PENDING = "PENDING"
    DEPENDENCY_CHECK = "DEPENDENCY_CHECK"
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    UNINSTALLED = "UNINSTALLED"

class MarketplaceInstallation(BaseModel):
    installation_id: str
    tenant_id: str
    product_id: str
    state: InstallationState = InstallationState.PENDING
    region: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InstallationManager:
    def __init__(self):
        self.installations: Dict[str, MarketplaceInstallation] = {}
        
    def start_installation(self, installation: MarketplaceInstallation) -> MarketplaceInstallation:
        self.installations[installation.installation_id] = installation
        return installation
        
    def update_state(self, installation_id: str, new_state: InstallationState) -> MarketplaceInstallation:
        if installation_id not in self.installations:
            raise ValueError("Installation not found")
        self.installations[installation_id].state = new_state
        return self.installations[installation_id]
