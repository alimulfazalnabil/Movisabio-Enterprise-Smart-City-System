from src.services.economy.models.schemas import EconomicActivityIndicator
from datetime import datetime

class EconomicActivityEngine:
    def calculate_composite_index(self, indicator: EconomicActivityIndicator) -> EconomicActivityIndicator:
        """
        Calculates the composite Territorial Economic Activity Indicator based on weighted components.
        """
        weights = {
            "business": 0.4,
            "retail": 0.3,
            "mobility": 0.15,
            "tourism": 0.15
        }
        
        index = (
            indicator.business_activity_score * weights["business"] +
            indicator.retail_activity_score * weights["retail"] +
            indicator.mobility_score * weights["mobility"] +
            indicator.tourism_score * weights["tourism"]
        )
        
        indicator.composite_index = round(index, 2)
        indicator.calculation_timestamp = datetime.utcnow()
        return indicator
