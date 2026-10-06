from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class ExtensionStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    VALIDATED = "VALIDATED"
    CERTIFIED = "CERTIFIED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"

class EcosystemExtension(BaseModel):
    extension_id: str
    publisher_id: str
    extension_type: str
    name: str
    version: str
    status: ExtensionStatus = ExtensionStatus.SUBMITTED
    risk_class: str = "R1"
    required_permissions: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExtensionRegistry:
    def __init__(self):
        self.extensions: Dict[str, EcosystemExtension] = {}
        
    def register_extension(self, extension: EcosystemExtension) -> EcosystemExtension:
        self.extensions[extension.extension_id] = extension
        return extension
        
    def certify_extension(self, extension_id: str) -> EcosystemExtension:
        if extension_id not in self.extensions:
            raise ValueError("Extension not found")
        self.extensions[extension_id].status = ExtensionStatus.CERTIFIED
        return self.extensions[extension_id]
