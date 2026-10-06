from pydantic import BaseModel
from typing import List

class OTARelease(BaseModel):
    release_id: str
    component: str # firmware, edge_ai_model
    version: str
    signature: str
    is_signed: bool = False
    
    def sign(self) -> None:
        self.is_signed = True
        
class OTADeployment:
    def __init__(self, release: OTARelease, target_devices: List[str]):
        self.release = release
        self.target_devices = target_devices
        self.status = "STAGING"
        
    def rollout(self) -> bool:
        if not self.release.is_signed:
            self.status = "FAILED_SIGNATURE"
            return False
            
        self.status = "ROLLOUT"
        return True
