import hashlib
import secrets

def generate_api_key(prefix: str = "ms_live_") -> tuple[str, str]:
    """
    Generates a new API key and its hash.
    Returns: (raw_key, hashed_key)
    """
    token = secrets.token_urlsafe(32)
    raw_key = f"{prefix}{token}"
    
    # We store the hash in the database
    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    
    return raw_key, hashed_key

def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    """
    Verifies if a raw API key matches the stored hash.
    """
    computed_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    return secrets.compare_digest(computed_hash, stored_hash)
