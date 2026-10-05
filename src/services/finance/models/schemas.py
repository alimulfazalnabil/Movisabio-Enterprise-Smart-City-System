from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class ProjectFinancialModel(BaseModel):
    project_id: str
    capex: float
    opex: float
    revenue: float
    maintenance: float
    financing_costs: float

class FinancialMetrics(BaseModel):
    project_id: str
    cash_flow: float
    npv: Optional[float] = None
    payback_period: Optional[float] = None

class InvestmentScenario(BaseModel):
    scenario_id: str
    project_id: str
    assumptions: Dict[str, float]

class EconomicShock(BaseModel):
    shock_id: str
    shock_type: str # FUEL_PRICE, FLOOD, CYBER
    magnitude: float

class ShockImpact(BaseModel):
    shock_id: str
    affected_sectors: List[str]
    estimated_economic_impact: float
