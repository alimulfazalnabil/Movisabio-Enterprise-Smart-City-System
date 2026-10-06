from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class SurveyStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    VALIDATED = "VALIDATED"

class SiteSurvey(BaseModel):
    survey_id: str
    project_id: str
    site_id: str
    status: SurveyStatus = SurveyStatus.PLANNED
    observations: Dict[str, Any] = Field(default_factory=dict)
    evidence_links: List[str] = Field(default_factory=list)
    surveyor_id: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SurveyEngine:
    def __init__(self):
        self.surveys: Dict[str, SiteSurvey] = {}
        
    def create_survey(self, survey: SiteSurvey) -> SiteSurvey:
        self.surveys[survey.survey_id] = survey
        return survey
        
    def complete_survey(self, survey_id: str, observations: Dict[str, Any]) -> SiteSurvey:
        if survey_id not in self.surveys:
            raise ValueError("Survey not found")
        self.surveys[survey_id].status = SurveyStatus.COMPLETED
        self.surveys[survey_id].observations.update(observations)
        return self.surveys[survey_id]
