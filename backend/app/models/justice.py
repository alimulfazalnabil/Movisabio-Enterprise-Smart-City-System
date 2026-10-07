from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class Court(Base):
    """B29.1 - Justice Intelligence Foundation"""
    __tablename__ = "courts"
    court_id = Column(String, primary_key=True)
    name = Column(String)
    jurisdiction = Column(String)
    type = Column(String) # CIVIL, CRIMINAL, ADMINISTRATIVE
    location_id = Column(String)
    capacity_score = Column(Float)

class LegalCase(Base):
    """B29.2 - Case Digital Twin"""
    __tablename__ = "legal_cases"
    case_id = Column(String, primary_key=True)
    court_id = Column(String, ForeignKey("courts.court_id"))
    case_type = Column(String)
    filing_date = Column(DateTime(timezone=True))
    status = Column(String) # INTAKE, HEARING, JUDGMENT, APPEAL
    applicable_rules = Column(JSON)
    privacy_classification = Column(String) # PUBLIC, RESTRICTED, SEALED

class ProceduralDeadline(Base):
    """B29.11 - Legal Deadline Intelligence"""
    __tablename__ = "procedural_deadlines"
    deadline_id = Column(String, primary_key=True)
    case_id = Column(String, ForeignKey("legal_cases.case_id"))
    rule_id = Column(String)
    event_type = Column(String)
    due_date = Column(DateTime(timezone=True))
    status = Column(String) # PENDING, MET, MISSED
