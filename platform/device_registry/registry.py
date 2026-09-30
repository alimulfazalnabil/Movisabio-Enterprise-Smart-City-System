from typing import Dict, Any
from datetime import datetime

class DeviceRegistry:
    """
    Centralized registry for every Edge node, CCTV, and controller 
    globally connected to the MoviSabio platform.
    """
    def __init__(self):
        self.devices = {}
        
    def register_device(self, tenant_id: str, device_id: str, device_type: str, metadata: Dict[str, Any]):
        self.devices[device_id] = {
            "tenant_id": tenant_id,
            "type": device_type,
            "metadata": metadata,
            "status": "ONLINE",
            "last_seen": datetime.utcnow().isoformat()
        }
        
    def heartbeat(self, device_id: str):
        if device_id in self.devices:
            self.devices[device_id]["last_seen"] = datetime.utcnow().isoformat()
            self.devices[device_id]["status"] = "ONLINE"
            
    def get_tenant_devices(self, tenant_id: str) -> Dict[str, Any]:
        return {k: v for k, v in self.devices.items() if v["tenant_id"] == tenant_id}
