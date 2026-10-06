from typing import Dict, Any, List

class SecurityValidator:
    def validate_extension(self, extension_manifest: Dict[str, Any]) -> bool:
        """
        Validates basic security constraints for an extension.
        """
        required_fields = ["name", "version", "publisher_id", "permissions"]
        if not all(field in extension_manifest for field in required_fields):
            return False
            
        permissions = extension_manifest.get("permissions", [])
        # R5 permissions are denied by default for external apps
        if "traffic.control" in permissions or "device.write" in permissions:
            return False
            
        return True
