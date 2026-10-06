from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class TechnologyStatus(str, enum.Enum):
    EVALUATE = "EVALUATE"
    EXPERIMENTAL = "EXPERIMENTAL"
    APPROVED = "APPROVED"
    PREFERRED = "PREFERRED"
    RESTRICTED = "RESTRICTED"
    DEPRECATED = "DEPRECATED"
    PROHIBITED = "PROHIBITED"
    RETIRED = "RETIRED"

class TechnologyItem(BaseModel):
    tech_id: str
    name: str
    domain: str
    status: TechnologyStatus = TechnologyStatus.EVALUATE
    review_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TechnologyPortfolio:
    def __init__(self):
        self.technologies: Dict[str, TechnologyItem] = {}
        
    def add_technology(self, tech: TechnologyItem) -> TechnologyItem:
        self.technologies[tech.tech_id] = tech
        return tech
        
    def update_status(self, tech_id: str, new_status: TechnologyStatus) -> TechnologyItem:
        if tech_id not in self.technologies:
            raise ValueError("Technology not found")
        tech = self.technologies[tech_id]
        tech.status = new_status
        return tech
