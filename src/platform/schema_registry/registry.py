from typing import Dict, Any, Optional

class SchemaVersion:
    def __init__(self, version: str, definition: Dict[str, Any]):
        self.version = version
        self.definition = definition

class SchemaRegistry:
    def __init__(self):
        # schema_id -> version -> definition
        self.schemas: Dict[str, Dict[str, SchemaVersion]] = {}
        
    def register_schema(self, schema_id: str, version: str, definition: Dict[str, Any]) -> None:
        if schema_id not in self.schemas:
            self.schemas[schema_id] = {}
        self.schemas[schema_id][version] = SchemaVersion(version, definition)
        
    def get_schema(self, schema_id: str, version: str) -> Optional[Dict[str, Any]]:
        schema = self.schemas.get(schema_id)
        if schema:
            ver = schema.get(version)
            if ver:
                return ver.definition
        return None
