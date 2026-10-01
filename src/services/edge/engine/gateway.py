from typing import Dict, Any
from src.services.edge.models.schemas import EdgeDevice

class EdgeGateway:
    """
    Handles local ingestion, device authentication, and schema validation.
    """
    
    def __init__(self):
        self.registered_devices: Dict[str, EdgeDevice] = {}
        
    def register_device(self, device: EdgeDevice):
        self.registered_devices[device.device_id] = device
        
    def authenticate_payload(self, device_id: str, cert_signature: str, payload: Dict[str, Any]) -> bool:
        """
        Validates device identity using mTLS/certificate abstraction.
        """
        if device_id not in self.registered_devices:
            return False
            
        device = self.registered_devices[device_id]
        if device.status != "ACTIVE":
            return False
            
        # Mocking signature verification
        if cert_signature != f"valid_sig_for_{device.certificate_id}":
            return False
            
        return True
