"""Standalone FastAPI service for issuing and validating access tokens."""

import os
import time
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MoviSabio.SecurityGateway")

app = FastAPI(
    title="MoviSabio Enterprise API Authentication & Security Gateway",
    version="1.0.0",
    description="Manages JWT token issuance, cryptographic verification, and Role-Based Access Control (RBAC)."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Cryptographic Configuration (In production, load securely from secret managers or environment variables)
SECRET_KEY = os.getenv("MOVISABIO_JWT_SECRET", "super_secret_enterprise_jwt_key_change_in_production_2026")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

security_scheme = HTTPBearer()

class TokenRequestPayload(BaseModel):
    """Credentials and requested role used to issue an access token."""

    client_id: str
    client_secret: str
    role: str  # e.g., "ADMIN", "MUNICIPAL_OPERATOR", "IOT_SERVICE_NODE"


class TokenVerificationResponse(BaseModel):
    """Validated token identity and role returned to callers."""

    valid: bool
    client_id: Optional[str] = None
    role: Optional[str] = None
    expires_at: Optional[float] = None


class SecurityGatewayEngine:
    """Handles cryptographic token generation, verification, and role-based access control."""
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_access_token(self, payload: TokenRequestPayload) -> Dict[str, Any]:
        """Generates a cryptographically signed JWT access token."""
        logger.info(f"Generating access token for client {payload.client_id} with role {payload.role}...")

        # Simple mock credential validation check
        if payload.client_secret != "movisabio_secure_secret_2026":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client secret credentials."
            )

        issued_at = time.time()
        expires_at = issued_at + (TOKEN_EXPIRE_MINUTES * 60)

        token_data = {
            "sub": payload.client_id,
            "role": payload.role,
            "iat": issued_at,
            "exp": expires_at
        }

        encoded_jwt = jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)

        response = {
            "access_token": encoded_jwt,
            "token_type": "bearer",
            "expires_in_seconds": TOKEN_EXPIRE_MINUTES * 60,
            "role": payload.role,
            "timestamp": issued_at
        }
        return response

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Decodes and cryptographically verifies JWT signature and expiration."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            client_id: str = payload.get("sub")
            role: str = payload.get("role")
            exp: float = payload.get("exp")

            if client_id is None or role is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token structure: missing claims."
                )

            return {
                "valid": True,
                "client_id": client_id,
                "role": role,
                "expires_at": exp
            }
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials or token expired."
            )


gateway_engine = SecurityGatewayEngine(secret_key=SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_role(credentials: HTTPAuthorizationCredentials = Security(security_scheme)) -> Dict[str, Any]:
    """Dependency injection helper to validate incoming bearer tokens on secure endpoints."""
    token = credentials.credentials
    verification = gateway_engine.verify_token(token)
    return verification


@app.post("/api/v1/auth/token", status_code=status.HTTP_200_OK)
def api_generate_token(payload: TokenRequestPayload):
    """API endpoint to authenticate clients and issue cryptographically signed JWT access tokens."""
    try:
        token_response = gateway_engine.generate_access_token(payload)
        
        # Cache active session token hash in Redis for token revocation auditing
        cache_key = f"auth:session:{payload.client_id}"
        redis_client.setex(cache_key, TOKEN_EXPIRE_MINUTES * 60, payload.role)

        return {
            "status": "success",
            "authentication": token_response
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Token generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/auth/verify", status_code=status.HTTP_200_OK)
def api_verify_token(user_info: Dict[str, Any] = Depends(get_current_user_role)):
    """API endpoint to verify the validity of bearer tokens and inspect role permissions."""
    return {
        "status": "success",
        "token_verification": user_info
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("security_gateway:app", host="0.0.0.0", port=8033, reload=True)
