from typing import Dict, Any, Optional
from datetime import datetime
from src.platform.identity.models import MoviIdentity

class DeviceIdentity(MoviIdentity):
    device_type: str
    certificate_id: str
    certificate_expiry: datetime
    site_id: str
    capabilities: list[str]

class DeviceRegistry:
    def __init__(self):
        self.devices: Dict[str, DeviceIdentity] = {}
        
    def register_device(self, device: DeviceIdentity) -> None:
        self.devices[device.identity_id] = device
        
    def get_device(self, identity_id: str) -> Optional[DeviceIdentity]:
        return self.devices.get(identity_id)
        
    def is_certificate_valid(self, identity_id: str, current_time: datetime) -> bool:
        device = self.get_device(identity_id)
        if not device:
            return False
        return device.certificate_expiry > current_time and device.status == "ACTIVE"
