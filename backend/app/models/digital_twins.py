from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class DigitalTwinIdentity(Base):
    """B41.3 - Digital Twin Identity & B41.4 - Twin Registry"""
    __tablename__ = "digital_twin_identities"
    twin_id = Column(String, primary_key=True) # e.g. twin://movisabio/de/berlin/traffic
    owner_org_id = Column(String)
    jurisdiction = Column(String)
    twin_level = Column(Integer) # 1: Asset, 2: System, 3: Facility, 4: Territory, 5: Global
    capabilities = Column(JSON)
    health_score = Column(Float)
    trust_status = Column(String) # VERIFIED, TRUSTED, RESTRICTED
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TwinFederationContract(Base):
    """B41.10 - Twin Synchronization Contracts"""
    __tablename__ = "twin_federation_contracts"
    contract_id = Column(String, primary_key=True)
    provider_twin_id = Column(String, ForeignKey("digital_twin_identities.twin_id"))
    consumer_twin_id = Column(String, ForeignKey("digital_twin_identities.twin_id"))
    data_schema = Column(String)
    update_frequency = Column(String)
    privacy_classification = Column(String)
    status = Column(String) # ACTIVE, SUSPENDED

class TwinStateProvenance(Base):
    """B41.20 - Digital Twin Provenance"""
    __tablename__ = "twin_state_provenance"
    provenance_id = Column(String, primary_key=True)
    twin_id = Column(String, ForeignKey("digital_twin_identities.twin_id"))
    state_class = Column(String) # OBSERVED, ESTIMATED, SIMULATED
    source_entity = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    metadata_json = Column(JSON)
