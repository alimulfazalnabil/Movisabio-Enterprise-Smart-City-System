from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class InvestmentStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"

class InvestmentOpportunity(BaseModel):
    investment_id: str
    name: str
    capital_required: float
    expected_value: float
    risk_score: float # 0.0 to 1.0
    strategic_alignment: float # 0.0 to 1.0
    status: InvestmentStatus = InvestmentStatus.PROPOSED

class PortfolioOptimizer:
    def __init__(self):
        self.opportunities: Dict[str, InvestmentOpportunity] = {}
        
    def add_opportunity(self, opportunity: InvestmentOpportunity) -> InvestmentOpportunity:
        self.opportunities[opportunity.investment_id] = opportunity
        return opportunity
        
    def optimize_portfolio(self, budget_constraint: float) -> List[InvestmentOpportunity]:
        # Simple greedy knapsack based on a risk-adjusted strategic score
        # Score = (Expected Value * Strategic Alignment) / (Capital * (1 + Risk))
        
        def calculate_score(opp: InvestmentOpportunity) -> float:
            if opp.capital_required == 0:
                return float('inf')
            return (opp.expected_value * opp.strategic_alignment) / (opp.capital_required * (1.0 + opp.risk_score))
            
        candidates = sorted(self.opportunities.values(), key=calculate_score, reverse=True)
        
        selected = []
        spent = 0.0
        
        for opp in candidates:
            if spent + opp.capital_required <= budget_constraint:
                opp.status = InvestmentStatus.APPROVED
                selected.append(opp)
                spent += opp.capital_required
            else:
                opp.status = InvestmentStatus.DEFERRED
                
        return selected
