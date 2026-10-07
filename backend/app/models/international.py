from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class TerritoryNode(Base):
    """B31.1 - Multi-Territory Operating Model"""
    __tablename__ = "territory_nodes"
    territory_id = Column(String, primary_key=True)
    name = Column(String)
    level = Column(String) # GLOBAL, COUNTRY, REGION, MUNICIPALITY
    parent_territory_id = Column(String)

class BorderGateway(Base):
    """B31.4 - Cross-Border Mobility Intelligence"""
    __tablename__ = "border_gateways"
    gateway_id = Column(String, primary_key=True)
    territory_a_id = Column(String, ForeignKey("territory_nodes.territory_id"))
    territory_b_id = Column(String, ForeignKey("territory_nodes.territory_id"))
    type = Column(String) # LAND_CUSTOMS, PORT, AIRPORT
    daily_capacity = Column(Integer)
    status = Column(String) # OPEN, RESTRICTED, CLOSED

class CrossBorderInfrastructure(Base):
    """B31.7 - Cross-Border Infrastructure Dependencies"""
    __tablename__ = "cross_border_infrastructure"
    asset_id = Column(String, primary_key=True)
    type = Column(String) # POWER_GRID, PIPELINE, RIVER
    territories_connected = Column(JSON) # List of territory IDs
    criticality = Column(String) # HIGH, MEDIUM, LOW

class TerritorialDataExchange(Base):
    """B31.3 - Cross-Border Data Exchange"""
    __tablename__ = "territorial_data_exchanges"
    exchange_id = Column(String, primary_key=True)
    source_territory_id = Column(String, ForeignKey("territory_nodes.territory_id"))
    destination_territory_id = Column(String, ForeignKey("territory_nodes.territory_id"))
    data_classification = Column(String)
    purpose = Column(String)
    authorized = Column(Boolean, default=False)
