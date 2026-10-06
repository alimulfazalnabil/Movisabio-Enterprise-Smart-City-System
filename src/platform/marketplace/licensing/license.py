from pydantic import BaseModel
from typing import List, Dict, Optional
import enum

class UsageRight(str, enum.Enum):
    VIEW = "VIEW"
    QUERY = "QUERY"
    DOWNLOAD = "DOWNLOAD"
    API_ACCESS = "API_ACCESS"
    ANALYTICS = "ANALYTICS"
    MODEL_TRAINING = "MODEL_TRAINING"
    COMMERCIALIZE = "COMMERCIALIZE"

class ProductLicense(BaseModel):
    license_id: str
    product_id: str
    allowed_rights: List[UsageRight]
    restricted_rights: List[UsageRight]
    
class EntitlementEngine:
    def __init__(self):
        self.licenses: Dict[str, ProductLicense] = {}
        
    def attach_license(self, license: ProductLicense):
        self.licenses[license.product_id] = license
        
    def verify_entitlement(self, product_id: str, requested_right: UsageRight) -> bool:
        if product_id not in self.licenses:
            return False
        license = self.licenses[product_id]
        if requested_right in license.restricted_rights:
            return False
        return requested_right in license.allowed_rights
