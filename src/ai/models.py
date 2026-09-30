from sqlalchemy import Column, String, JSON, Boolean
from src.core.models import BaseEntity, generate_ulid_like_id

class AIModel(BaseEntity):
    """
    Registry of deployed AI models (e.g. YOLOv8, RL Optimizer).
    """
    __tablename__ = "ai_models"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("model"))
    name = Column(String, nullable=False)
    model_type = Column(String, nullable=False) # PERCEPTION, PREDICTION, OPTIMIZATION
    description = Column(String, nullable=True)

class AIModelVersion(BaseEntity):
    """
    Specific version of a model, its weights URI, and its parameters.
    """
    __tablename__ = "ai_model_versions"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("modver"))
    model_id = Column(String, nullable=False)
    version_tag = Column(String, nullable=False)
    
    weights_uri = Column(String, nullable=True) # Object storage URI
    hyperparameters = Column(JSON, nullable=True)
    
    is_active_production = Column(Boolean, default=False)
    is_active_shadow = Column(Boolean, default=False)
