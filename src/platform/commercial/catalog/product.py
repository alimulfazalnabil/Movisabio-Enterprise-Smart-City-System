from pydantic import BaseModel
from typing import Dict, List, Optional

class Feature(BaseModel):
    feature_id: str
    name: str
    description: str

class Module(BaseModel):
    module_id: str
    name: str
    features: List[Feature]

class Product(BaseModel):
    product_id: str
    product_code: str
    name: str
    modules: List[Module]

class Catalog:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        
    def add_product(self, product: Product) -> None:
        self.products[product.product_id] = product
        
    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)
