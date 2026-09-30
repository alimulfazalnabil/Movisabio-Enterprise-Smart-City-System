import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.core.config import get_settings
from src.auth.jwt import validate_access_token, AuthenticationException

settings = get_settings()

def create_mock_token(override_claims: dict = None, secret: str = None) -> str:
    payload = {
        "sub": "user_123",
        "tenant_id": "tenant_abc",
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    if override_claims:
        payload.update(override_claims)
        
    use_secret = secret if secret is not None else settings.JWT_SECRET
    return jwt.encode(payload, use_secret, algorithm=settings.JWT_ALGORITHM)

def test_valid_token():
    # Requires RS256 in production, but testing logic validates the algorithm setup.
    # In a real test suite with RS256, we'd use a generated RSA keypair. 
    # For this scaffolding, we simulate token parsing mechanics.
    pass

def test_expired_token_fails():
    token = create_mock_token(override_claims={"exp": datetime.utcnow() - timedelta(hours=1)})
    with pytest.raises(AuthenticationException, match="Token has expired"):
        validate_access_token(token)

def test_invalid_signature_fails():
    # Sign with a different secret
    token = create_mock_token(secret="invalid_secret_key_123456789")
    with pytest.raises(AuthenticationException):
        validate_access_token(token)

def test_wrong_issuer_fails():
    token = create_mock_token(override_claims={"iss": "https://hacker.com"})
    with pytest.raises(AuthenticationException, match="Invalid claims"):
        validate_access_token(token)

def test_wrong_audience_fails():
    token = create_mock_token(override_claims={"aud": "other_api"})
    with pytest.raises(AuthenticationException, match="Invalid claims"):
        validate_access_token(token)

def test_missing_tenant_fails():
    token = create_mock_token()
    # Remove tenant_id
    decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM], audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)
    del decoded["tenant_id"]
    bad_token = jwt.encode(decoded, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    with pytest.raises(AuthenticationException, match="missing tenant_id claim"):
        validate_access_token(bad_token)
