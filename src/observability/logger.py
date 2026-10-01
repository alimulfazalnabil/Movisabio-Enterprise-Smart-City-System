import logging
import json
from datetime import datetime
from src.core.context import get_trace_context, get_tenant_context, get_user_context
from src.core.config import get_settings

settings = get_settings()

class ContextAwareJSONFormatter(logging.Formatter):
    """
    JSON formatter that automatically injects tenant, request, and correlation contexts
    into every log statement.
    """
    def format(self, record: logging.LogRecord) -> str:
        trace_context = get_trace_context()
        tenant_id = get_tenant_context()
        user_id = get_user_context()
        
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": getattr(record, "service", "movisabio-api"),
            "environment": settings.ENVIRONMENT,
            "tenant_id": tenant_id,
            "user_id": user_id,
            "request_id": trace_context.get("request_id"),
            "correlation_id": trace_context.get("correlation_id"),
            "event": record.getMessage(),
        }
        
        # Merge any 'extra' kwargs passed to the logger
        if hasattr(record, "extra_attrs"):
            for key, value in record.extra_attrs.items():
                log_obj[key] = value
                
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_obj)

def setup_logging():
    logger = logging.getLogger("movisabio")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicating handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(ContextAwareJSONFormatter())
        logger.addHandler(handler)
    
    return logger

def get_logger():
    return logging.getLogger("movisabio")
