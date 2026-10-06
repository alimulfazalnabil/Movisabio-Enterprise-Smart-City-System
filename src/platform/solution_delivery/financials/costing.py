from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class ProjectFinancials(BaseModel):
    project_id: str
    planned_cost: float = 0.0
    actual_cost: float = 0.0
    planned_revenue: float = 0.0
    actual_revenue: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def gross_margin(self) -> float:
        if self.actual_revenue == 0.0:
            return 0.0
        return ((self.actual_revenue - self.actual_cost) / self.actual_revenue) * 100.0

class FinancialEngine:
    def __init__(self):
        self.financials: Dict[str, ProjectFinancials] = {}
        
    def initialize_project(self, project_id: str, planned_cost: float, planned_revenue: float) -> ProjectFinancials:
        record = ProjectFinancials(
            project_id=project_id,
            planned_cost=planned_cost,
            planned_revenue=planned_revenue
        )
        self.financials[project_id] = record
        return record
        
    def add_cost(self, project_id: str, amount: float) -> ProjectFinancials:
        if project_id not in self.financials:
            raise ValueError("Financial record not found")
        self.financials[project_id].actual_cost += amount
        return self.financials[project_id]
