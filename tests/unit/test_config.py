import pytest
import os
from pydantic import ValidationError
from src.core.config import Settings

def test_development_config_loads():
    settings = Settings(
        APP_ENV="development",
        DATABASE_URL="postgresql://user:pass@localhost/db",
        REDIS_URL="redis://localhost",
        JWT_SECRET="secret"
    )
    assert settings.APP_ENV == "development"
    assert settings.TRAFFIC_CONTROLLER_MODE == "simulation"

def test_missing_required_variable_fails():
    with pytest.raises(ValidationError):
        Settings(APP_ENV="development", REDIS_URL="redis://localhost") # Missing DATABASE_URL and JWT_SECRET

def test_unsafe_production_config_fails():
    with pytest.raises(ValueError, match="DEBUG mode cannot be enabled in production"):
        Settings(
            APP_ENV="production",
            DEBUG=True,
            DATABASE_URL="postgresql://user:pass@localhost/db",
            REDIS_URL="redis://localhost",
            JWT_SECRET="secret"
        )

def test_invalid_production_cors_fails():
    with pytest.raises(ValueError, match="CORS_ORIGINS must be strictly defined in production"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            DATABASE_URL="postgresql://user:pass@localhost/db",
            REDIS_URL="redis://localhost",
            JWT_SECRET="secret",
            CORS_ORIGINS=["*"]
        )

def test_traffic_control_safety_enforced():
    with pytest.raises(ValueError, match="CRITICAL SAFETY ERROR"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            DATABASE_URL="postgresql://user:pass@localhost/db",
            REDIS_URL="redis://localhost",
            JWT_SECRET="secret",
            CORS_ORIGINS=["https://movisabio.com"],
            TRAFFIC_CONTROLLER_MODE="live",
            SAFETY_VALIDATION=False
        )
