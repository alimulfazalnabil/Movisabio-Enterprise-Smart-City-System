from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class TerritorialDigitalMaturity(Base):
    """B38.3 - Digital Transformation Intelligence"""
    __tablename__ = "territorial_digital_maturity"
    maturity_id = Column(String, primary_key=True)
    territory_id = Column(String)
    overall_maturity_score = Column(Float)
    infrastructure_readiness = Column(Float)
    workforce_skill_level = Column(Float)
    business_technology_adoption = Column(Float)
    digital_public_services = Column(Float)
    last_assessed = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DigitalWorkforceSkillGap(Base):
    """B38.7 - Digital Skill Gap Intelligence"""
    __tablename__ = "digital_skill_gaps"
    gap_id = Column(String, primary_key=True)
    territory_id = Column(String)
    skill_domain = Column(String) # CLOUD, AI, CYBERSECURITY, DATA
    current_supply = Column(Integer)
    projected_demand = Column(Integer)
    gap_magnitude = Column(Integer)
    criticality = Column(String) # HIGH, MEDIUM, LOW

class TechnologyAdoption(Base):
    """B38.5 - Technology Adoption Intelligence"""
    __tablename__ = "technology_adoption_metrics"
    adoption_id = Column(String, primary_key=True)
    territory_id = Column(String)
    technology_category = Column(String) # AI, IOT, ROBOTICS, CLOUD
    adoption_rate_pct = Column(Float)
    primary_adopter_sectors = Column(JSON) # e.g. ["Manufacturing", "Finance"]
    adoption_barrier = Column(String) # SKILLS, CAPITAL, INFRASTRUCTURE
