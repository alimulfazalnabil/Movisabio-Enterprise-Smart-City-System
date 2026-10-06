from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class ROIModel(BaseModel):
    roi_id: str
    tenant_id: str
    investment: float
    net_benefit: float = 0.0
    avoided_costs: float = 0.0
    incremental_revenue: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def total_benefit(self) -> float:
        return self.net_benefit + self.avoided_costs + self.incremental_revenue
        
    @property
    def roi_percentage(self) -> float:
        if self.investment == 0:
            return 0.0
        return ((self.total_benefit - self.investment) / self.investment) * 100.0

class ValueEngine:
    def __init__(self):
        self.roi_models: Dict[str, ROIModel] = {}
        
    def create_roi_model(self, model: ROIModel) -> ROIModel:
        self.roi_models[model.roi_id] = model
        return model
        
    def update_benefits(self, roi_id: str, net_benefit: float, avoided_costs: float, incremental_revenue: float) -> ROIModel:
        if roi_id not in self.roi_models:
            raise ValueError("ROI Model not found")
        model = self.roi_models[roi_id]
        model.net_benefit = net_benefit
        model.avoided_costs = avoided_costs
        model.incremental_revenue = incremental_revenue
        return model
