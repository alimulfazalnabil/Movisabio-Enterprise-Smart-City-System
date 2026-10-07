from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class TerritorialEquityProfile(Base):
    """B36.4 - Territorial Equity Model"""
    __tablename__ = "territorial_equity_profiles"
    profile_id = Column(String, primary_key=True)
    territory_id = Column(String)
    composite_equity_score = Column(Float)
    service_accessibility_index = Column(Float)
    environmental_burden_index = Column(Float)
    economic_opportunity_index = Column(Float)
    digital_inclusion_index = Column(Float)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ServiceAccessibility(Base):
    """B36.5 - Access-to-Service Intelligence"""
    __tablename__ = "service_accessibility"
    accessibility_id = Column(String, primary_key=True)
    territory_id = Column(String)
    service_type = Column(String) # HEALTHCARE, EDUCATION, TRANSPORT
    average_travel_time_mins = Column(Float)
    population_coverage_pct = Column(Float)
    capacity_constraint = Column(Boolean)

class CommunityFeedback(Base):
    """B36.20 - Civic Feedback Intelligence"""
    __tablename__ = "community_feedback"
    feedback_id = Column(String, primary_key=True)
    territory_id = Column(String)
    topic_category = Column(String) # HOUSING, TRANSPORT, SAFETY, ENVIRONMENT
    sentiment_score = Column(Float) # 0 to 1
    frequency_count = Column(Integer)
    status = Column(String) # EMERGING_ISSUE, RECURRING_ISSUE, RESOLVED
