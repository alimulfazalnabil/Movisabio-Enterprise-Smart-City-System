from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base

class DemographicProfile(Base):
    """B35.1 - Population Intelligence Model"""
    __tablename__ = "demographic_profiles"
    profile_id = Column(String, primary_key=True)
    territory_id = Column(String)
    total_population = Column(Integer)
    age_structure = Column(JSON) # e.g. {"0-14": 20, "15-64": 65, "65+": 15}
    household_structure = Column(JSON)
    population_density = Column(Float)
    reference_year = Column(Integer)

class MigrationFlow(Base):
    """B35.5 - Migration Intelligence"""
    __tablename__ = "migration_flows"
    flow_id = Column(String, primary_key=True)
    origin_territory_id = Column(String)
    destination_territory_id = Column(String)
    estimated_volume = Column(Integer)
    primary_driver = Column(String) # ECONOMIC, CLIMATE, CONFLICT
    timeframe = Column(String) # e.g. "2025-2030"

class ServiceDemandProjection(Base):
    """B35.12 - Population-Service Demand Model"""
    __tablename__ = "service_demand_projections"
    projection_id = Column(String, primary_key=True)
    territory_id = Column(String)
    service_type = Column(String) # EDUCATION, HEALTHCARE, HOUSING, TRANSPORT
    scenario = Column(String) # BASELINE, HIGH_GROWTH, AGING
    projected_demand_metric = Column(Float)
    current_capacity = Column(Float)
    capacity_gap = Column(Float)
