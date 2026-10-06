from typing import List, Dict, Any, Optional
from src.platform.marketplace.catalog.product import ProductCatalog, MarketplaceProduct, ProductState

class MarketplaceSearch:
    def __init__(self, catalog: ProductCatalog):
        self.catalog = catalog
        
    def search(self, 
               query: Optional[str] = None, 
               category: Optional[str] = None, 
               region: Optional[str] = None,
               only_published: bool = True) -> List[MarketplaceProduct]:
        results = []
        for product in self.catalog.products.values():
            if only_published and product.state != ProductState.PUBLISHED:
                continue
                
            if category and product.category != category:
                continue
                
            if region and region not in product.regions and "GLOBAL" not in product.regions:
                continue
                
            if query and query.lower() not in product.name.lower():
                continue
                
            results.append(product)
            
        return results
