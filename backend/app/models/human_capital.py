from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class EducationInstitution(Base):
    """B20.2 - Education Infrastructure Intelligence"""
    __tablename__ = "education_institutions"
    institution_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # School, University, Vocational
    location = Column(Geometry('POINT'))
    student_capacity = Column(Integer)
    current_enrollment = Column(Integer)
    programs_offered = Column(JSON)

class Skill(Base):
    """B20.5 - Skills Intelligence Foundation"""
    __tablename__ = "skills"
    skill_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String) # Software, Engineering, Healthcare
    related_skills = Column(JSON)
    active_workforce_count = Column(Integer)

class OccupationDemand(Base):
    """B20.6 - Job & Occupation Intelligence"""
    __tablename__ = "occupation_demand"
    demand_id = Column(String, primary_key=True)
    occupation_name = Column(String)
    industry = Column(String)
    required_skills = Column(JSON)
    current_openings = Column(Integer)
    projected_growth_pct = Column(Float)
