from typing import Dict

class CostCalculator:
    def __init__(self):
        self.pricing_catalog: Dict[str, float] = {
            "gpu_seconds": 0.0004,
            "api_requests": 0.00001,
            "storage_gb_month": 0.02
        }
        
    def calculate_cost(self, resource_type: str, quantity: float) -> float:
        rate = self.pricing_catalog.get(resource_type, 0.0)
        return rate * quantity
        
    def set_price(self, resource_type: str, price: float) -> None:
        self.pricing_catalog[resource_type] = price
