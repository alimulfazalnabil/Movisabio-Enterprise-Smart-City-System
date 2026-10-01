from datetime import datetime, timezone
from src.services.v2x.models.schemas import V2XMessage, TrustState

class V2XGateway:
    """
    Ingests and validates incoming V2X messages (Replay Protection, Trust).
    """
    
    def validate_message(self, message: V2XMessage) -> TrustState:
        """
        Validates timestamp freshness and signature to determine TrustState.
        """
        now = datetime.now(timezone.utc)
        
        # Check freshness (e.g. older than 2 seconds is suspicious/rejected)
        age_seconds = (now - message.timestamp).total_seconds()
        
        if age_seconds > 5.0:
            return TrustState.REJECTED
        if age_seconds > 2.0:
            return TrustState.SUSPICIOUS
            
        # Mock Signature Validation
        if message.signature != f"valid_sig_{message.asset_id}":
            return TrustState.REJECTED
            
        return TrustState.TRUSTED
