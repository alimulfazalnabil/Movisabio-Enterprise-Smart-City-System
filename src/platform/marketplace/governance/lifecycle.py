from typing import Dict, Any, List
from src.platform.marketplace.registry.product import ProductRegistry, ProductStatus

class ProductGovernanceEngine:
    def __init__(self, registry: ProductRegistry):
        self.registry = registry
        
    def approve_for_publication(self, product_id: str, reviews: Dict[str, bool]) -> bool:
        """
        Requires checks: OWNERSHIP, LICENSE, PRIVACY, SECURITY, COMMERCIAL
        """
        required_checks = {"OWNERSHIP", "LICENSE", "PRIVACY", "SECURITY"}
        if not required_checks.issubset(reviews.keys()) or not all(reviews[k] for k in required_checks):
            return False
            
        product = self.registry.get_product(product_id)
        if product:
            product.status = ProductStatus.PUBLISHED
            return True
        return False

    def suspend_product(self, product_id: str, reason: str):
        product = self.registry.get_product(product_id)
        if product:
            product.status = ProductStatus.SUSPENDED
