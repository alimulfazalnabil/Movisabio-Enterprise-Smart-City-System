from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class PortfolioHealth(str, enum.Enum):
    HEALTHY = "HEALTHY"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    BLOCKED = "BLOCKED"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"

class PortfolioItem(BaseModel):
    item_id: str
    name: str
    item_type: str # PROGRAM, INITIATIVE, PROJECT
    strategic_objective_id: str
    health: PortfolioHealth = PortfolioHealth.UNKNOWN
    budget_allocated: float = 0.0
    budget_spent: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PortfolioEngine:
    def __init__(self):
        self.items: Dict[str, PortfolioItem] = {}
        
    def add_item(self, item: PortfolioItem) -> PortfolioItem:
        self.items[item.item_id] = item
        return item
        
    def evaluate_health(self, item_id: str) -> PortfolioItem:
        if item_id not in self.items:
            raise ValueError("Item not found")
            
        item = self.items[item_id]
        if item.health in [PortfolioHealth.COMPLETED, PortfolioHealth.CANCELLED, PortfolioHealth.PAUSED, PortfolioHealth.BLOCKED]:
            return item
            
        # Basic budget evaluation logic
        if item.budget_spent > item.budget_allocated:
            item.health = PortfolioHealth.CRITICAL
        elif item.budget_spent > item.budget_allocated * 0.9:
            item.health = PortfolioHealth.AT_RISK
        else:
            item.health = PortfolioHealth.HEALTHY
            
        return item
