from jose import jwt, JWTError
from datetime import datetime
from src.core.config import get_settings
from src.core.exceptions import MoviSabioException

settings = get_settings()

class AuthenticationException(MoviSabioException):
    def __init__(self, message: str = "Valid authentication is required."):
        super().__init__("AUTHENTICATION_REQUIRED", message, 401)

def validate_access_token(token: str) -> dict:
    """
    Validates the enterprise JWT token ensuring signature, issuer, audience, and expiration.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER
        )
        
        # Check standard claims
        if "sub" not in payload:
            raise AuthenticationException("Invalid token: missing subject claim.")
            
        if "tenant_id" not in payload:
            raise AuthenticationException("Invalid token: missing tenant_id claim.")
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise AuthenticationException("Token has expired.")
    except jwt.JWTClaimsError as e:
        raise AuthenticationException(f"Invalid claims: {str(e)}")
    except JWTError as e:
        raise AuthenticationException("Could not validate credentials.")

def get_tenant_from_token(payload: dict) -> str:
    return payload.get("tenant_id")
