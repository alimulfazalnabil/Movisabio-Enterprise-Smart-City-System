from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import enum

class ProductType(str, enum.Enum):
    DATASET = "DATASET"
    MODEL = "MODEL"
    AGENT = "AGENT"
    DIGITAL_TWIN = "DIGITAL_TWIN"
    SIMULATION = "SIMULATION"
    INTELLIGENCE = "INTELLIGENCE"

class ProductStatus(str, enum.Enum):
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"
    SUSPENDED = "SUSPENDED"

class MarketplaceProduct(BaseModel):
    product_id: str
    tenant_id: str
    product_type: ProductType
    name: str
    description: str
    owner_id: str
    provider_id: str
    status: ProductStatus = ProductStatus.REGISTERED
    version: str = "1.0"
    quality_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductRegistry:
    def __init__(self):
        self.products: Dict[str, MarketplaceProduct] = {}
        
    def register_product(self, product: MarketplaceProduct) -> MarketplaceProduct:
        self.products[product.product_id] = product
        return product
        
    def get_product(self, product_id: str) -> Optional[MarketplaceProduct]:
        return self.products.get(product_id)
