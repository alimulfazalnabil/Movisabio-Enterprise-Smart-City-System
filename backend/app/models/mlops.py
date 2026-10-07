from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class DatasetCatalog(Base):
    """B47.4 - Dataset Management & B47.5 Versioning"""
    __tablename__ = "mlops_datasets"
    dataset_id = Column(String, primary_key=True)
    name = Column(String)
    version = Column(String)
    lineage_source = Column(String)
    quality_score = Column(Float)
    schema_definition = Column(JSON)
    status = Column(String) # RAW, VALIDATED, APPROVED, RETIRED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class FeatureStore(Base):
    """B47.8 - Feature Store & B47.10 Consistency"""
    __tablename__ = "mlops_feature_store"
    feature_id = Column(String, primary_key=True)
    name = Column(String) # e.g. "average_speed_5min"
    calculation_logic = Column(String)
    update_frequency = Column(String)
    is_online = Column(Boolean, default=True)
    is_offline = Column(Boolean, default=True)
    lineage = Column(JSON)

class ModelRegistry(Base):
    """B47.15 - Model Registry & B47.16 Model Cards"""
    __tablename__ = "mlops_model_registry"
    model_id = Column(String, primary_key=True)
    name = Column(String)
    version = Column(String)
    dataset_id = Column(String, ForeignKey("mlops_datasets.dataset_id"))
    architecture = Column(String)
    status = Column(String) # DEVELOPMENT, VALIDATED, PRODUCTION, DEPRECATED
    performance_metrics = Column(JSON)
    governance_approval_id = Column(String) # Link to B46

class TrainingPipeline(Base):
    """B47.13 - Training Pipeline & B47.35 Retraining"""
    __tablename__ = "mlops_training_pipelines"
    job_id = Column(String, primary_key=True)
    model_name = Column(String)
    dataset_id = Column(String, ForeignKey("mlops_datasets.dataset_id"))
    hyperparameters = Column(JSON)
    gpu_allocation = Column(String)
    status = Column(String) # QUEUED, TRAINING, EVALUATING, COMPLETED, FAILED
    artifacts_uri = Column(String)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ModelDeployment(Base):
    """B47.20 - Deployment Architecture & B47.33 Monitoring"""
    __tablename__ = "mlops_deployments"
    deployment_id = Column(String, primary_key=True)
    model_id = Column(String, ForeignKey("mlops_model_registry.model_id"))
    routing_strategy = Column(String) # CANARY, SHADOW, BLUE_GREEN, STABLE
    traffic_percentage = Column(Float)
    target_environment = Column(String) # CLOUD_GPU, EDGE_GATEWAY
    status = Column(String) # DEPLOYING, ACTIVE, DEGRADED, ROLLED_BACK
    drift_score = Column(Float, default=0.0)
