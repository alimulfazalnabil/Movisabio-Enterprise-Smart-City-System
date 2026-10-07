from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class ResearchInstitution(Base):
    """B37.3 - Research Institution Intelligence"""
    __tablename__ = "research_institutions"
    institution_id = Column(String, primary_key=True)
    territory_id = Column(String)
    name = Column(String)
    institution_type = Column(String) # UNIVERSITY, NATIONAL_LAB, CORPORATE_R&D
    research_areas = Column(JSON) # e.g. ["Quantum Computing", "Biotech"]
    researcher_count = Column(Integer)
    annual_funding_usd = Column(Float)
    patent_count = Column(Integer)

class InnovationCluster(Base):
    """B37.18 - Innovation Cluster Intelligence"""
    __tablename__ = "innovation_clusters"
    cluster_id = Column(String, primary_key=True)
    territory_id = Column(String)
    domain = Column(String) # AI, AEROSPACE, FINTECH
    maturity_stage = Column(String) # EMERGING, GROWING, MATURE
    startup_density = Column(Float)
    venture_capital_deployed_usd = Column(Float)
    talent_gap_index = Column(Float)

class TechnologyTransfer(Base):
    """B37.17 - University-Industry Intelligence"""
    __tablename__ = "technology_transfers"
    transfer_id = Column(String, primary_key=True)
    source_institution_id = Column(String, ForeignKey("research_institutions.institution_id"))
    industry_partner = Column(String)
    technology_domain = Column(String)
    trl_level = Column(Integer) # 1 through 9
    commercialization_status = Column(String) # PROTOTYPE, PILOT, MARKET
