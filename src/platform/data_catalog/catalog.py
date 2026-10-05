from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class DataProduct(BaseModel):
    product_id: str
    name: str
    owner: str
    classification: str # PUBLIC, INTERNAL, RESTRICTED, CONFIDENTIAL, SENSITIVE, CRITICAL
    version: str
    schema_id: str
    description: str
    retention_policy: str
    dependencies: List[str] = Field(default_factory=list)

class DataCatalog:
    def __init__(self):
        self.products: Dict[str, DataProduct] = {}
        
    def register_product(self, product: DataProduct) -> None:
        self.products[product.product_id] = product
        
    def get_product(self, product_id: str) -> Optional[DataProduct]:
        return self.products.get(product_id)
        
    def search_products(self, query: str) -> List[DataProduct]:
        query = query.lower()
        return [
            p for p in self.products.values()
            if query in p.name.lower() or query in p.description.lower()
        ]
