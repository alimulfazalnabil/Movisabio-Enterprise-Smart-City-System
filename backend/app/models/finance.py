from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class InvestmentProject(Base):
    """B27.15 - Public Investment Optimization"""
    __tablename__ = "investment_projects"
    project_id = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String) # INFRASTRUCTURE, DIGITAL, ENERGY, MOBILITY
    capital_cost = Column(Float)
    expected_economic_value = Column(Float)
    expected_public_value = Column(Float)
    resilience_score = Column(Float)
    status = Column(String) # PROPOSED, APPROVED, ACTIVE

class PublicBudget(Base):
    """B27.13 - Public Finance Intelligence"""
    __tablename__ = "public_budgets"
    budget_id = Column(String, primary_key=True)
    jurisdiction = Column(String)
    fiscal_year = Column(Integer)
    total_revenue = Column(Float)
    total_expenditure = Column(Float)
    capital_investment = Column(Float)

class TradeFlow(Base):
    """B27.21 - Trade Intelligence"""
    __tablename__ = "trade_flows"
    flow_id = Column(String, primary_key=True)
    commodity = Column(String)
    origin_zone = Column(String)
    destination_zone = Column(String)
    volume_tons = Column(Float)
    value_usd = Column(Float)
    status = Column(String) # NORMAL, DISRUPTED

class FinancialActivityAggregate(Base):
    """B27.6 - Territorial Consumer Spending Intelligence"""
    __tablename__ = "financial_activity_aggregates"
    activity_id = Column(String, primary_key=True)
    zone_id = Column(String)
    sector = Column(String)
    timestamp = Column(DateTime(timezone=True))
    transaction_volume = Column(Float)
    growth_rate = Column(Float)
