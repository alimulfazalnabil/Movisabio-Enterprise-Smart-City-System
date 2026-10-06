from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class RequestContext(BaseModel):
    request_id: str
    tenant_id: str
    partner_id: Optional[str] = None
    identity_id: str
    scopes: List[str]
    timestamp: datetime

class RateLimiter:
    def __init__(self):
        # Simplified rate limiter mapping partner_id to usage count
        self.usage: Dict[str, int] = {}
        self.limits: Dict[str, int] = {
            "PUBLIC": 100,
            "PARTNER": 1000,
            "ENTERPRISE": 10000
        }
        
    def check_limit(self, partner_id: str, tier: str) -> bool:
        current = self.usage.get(partner_id, 0)
        limit = self.limits.get(tier, 0)
        
        if current >= limit:
            return False
            
        self.usage[partner_id] = current + 1
        return True

class APIGateway:
    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter
        
    def handle_request(self, context: RequestContext, required_scope: str, tier: str = "PUBLIC") -> Dict:
        """
        Validates rate limits and scopes before routing request.
        """
        # 1. Rate Limiting
        if context.partner_id:
            if not self.rate_limiter.check_limit(context.partner_id, tier):
                return {
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests",
                        "request_id": context.request_id
                    }
                }
                
        # 2. Scope Validation
        if required_scope not in context.scopes:
            return {
                "error": {
                    "code": "INSUFFICIENT_SCOPE",
                    "message": f"Requires scope: {required_scope}",
                    "request_id": context.request_id
                }
            }
            
        # 3. Success (Route to internal service)
        return {
            "data": {"status": "SUCCESS"},
            "meta": {
                "request_id": context.request_id,
                "timestamp": context.timestamp.isoformat()
            }
        }
