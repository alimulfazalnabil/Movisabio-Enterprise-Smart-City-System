from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class UIExtension(BaseModel):
    extension_id: str
    application_id: str
    type: str  # e.g. "widget", "map_layer"
    name: str
    config: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UIExtensionRegistry:
    def __init__(self):
        self.extensions: Dict[str, UIExtension] = {}
        
    def register_extension(self, extension: UIExtension) -> UIExtension:
        self.extensions[extension.extension_id] = extension
        return extension
        
    def get_extensions_by_type(self, type: str) -> List[UIExtension]:
        return [ext for ext in self.extensions.values() if ext.type == type]
