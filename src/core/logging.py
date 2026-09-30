import logging
import json
import datetime
from src.core.config import get_settings

settings = get_settings()

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": getattr(record, "service", settings.APP_NAME),
            "event": record.getMessage(),
        }
        
        # Inject standard contextual fields if they exist on the record
        for field in ["tenant_id", "intersection_id", "controller_id", "command_id", "trace_id", "request_id", "user_id"]:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)
                
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging():
    logger = logging.getLogger("movisabio")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = StructuredFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logging()
