from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class ProductState(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    VALIDATING = "VALIDATING"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    CERTIFIED = "CERTIFIED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"
    SUSPENDED = "SUSPENDED"

class ProductType(str, enum.Enum):
    APPLICATION = "APPLICATION"
    DATA = "DATA"
    MODEL = "MODEL"
    AGENT = "AGENT"
    DIGITAL_TWIN = "DIGITAL_TWIN"
    SERVICE = "SERVICE"

class MarketplaceProduct(BaseModel):
    product_id: str
    publisher_id: str
    name: str
    product_type: ProductType
    category: str
    state: ProductState = ProductState.DRAFT
    pricing: Dict[str, Any] = Field(default_factory=dict)
    regions: List[str] = Field(default_factory=list)
    risk_class: str = "R1"
    dependencies: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCatalog:
    def __init__(self):
        self.products: Dict[str, MarketplaceProduct] = {}
        
    def register_product(self, product: MarketplaceProduct) -> MarketplaceProduct:
        self.products[product.product_id] = product
        return product
        
    def update_state(self, product_id: str, new_state: ProductState) -> MarketplaceProduct:
        if product_id not in self.products:
            raise ValueError("Product not found")
        self.products[product_id].state = new_state
        return self.products[product_id]
