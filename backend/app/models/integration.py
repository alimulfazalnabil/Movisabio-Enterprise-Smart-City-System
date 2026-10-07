from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class EventEnvelope(Base):
    """B48.8 - Canonical Event Envelope"""
    __tablename__ = "integration_events"
    event_id = Column(String, primary_key=True)
    event_type = Column(String) # e.g. "traffic.state.updated"
    event_version = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    producer = Column(String)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    territory_id = Column(String)
    correlation_id = Column(String)
    causation_id = Column(String)
    classification = Column(String)
    schema_id = Column(String)
    payload = Column(JSON)

class IntegrationConnector(Base):
    """B48.29 - Connector Framework"""
    __tablename__ = "integration_connectors"
    connector_id = Column(String, primary_key=True)
    name = Column(String)
    connector_type = Column(String) # GIS, SCADA, ERP, IOT, TRANSIT
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    auth_config = Column(JSON)
    mapping_config = Column(JSON)
    status = Column(String) # ACTIVE, DEGRADED, OFFLINE, SUSPENDED
    last_sync = Column(DateTime)

class SchemaRegistry(Base):
    """B48.12 - Schema Registry"""
    __tablename__ = "integration_schemas"
    schema_id = Column(String, primary_key=True)
    domain = Column(String)
    version = Column(String)
    owner = Column(String)
    format = Column(String) # JSONSchema, Avro, Protobuf, GeoJSON
    definition = Column(JSON)
    status = Column(String) # DRAFT, STABLE, DEPRECATED

class IntegrationWorkflow(Base):
    """B48.26 - Workflow Orchestration"""
    __tablename__ = "integration_workflows"
    workflow_id = Column(String, primary_key=True)
    name = Column(String)
    trigger_event = Column(String)
    steps = Column(JSON)
    status = Column(String) # ACTIVE, PAUSED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
