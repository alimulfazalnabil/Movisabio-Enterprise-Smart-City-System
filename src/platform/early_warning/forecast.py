from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import enum

class WarningLevel(str, enum.Enum):
    WATCH = "WATCH"
    ADVISORY = "ADVISORY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ENDED = "ENDED"

class EventForecast(BaseModel):
    event_type: str
    expected_window_start: datetime
    expected_window_end: datetime
    location: str
    probability: float
    potential_severity: str

class EarlyWarningEngine:
    def evaluate_forecast(self, forecast: EventForecast) -> Optional[Dict]:
        """
        Escalates a forecast into a proactive early warning if thresholds are met.
        """
        if forecast.probability > 0.80 and forecast.potential_severity in ["HIGH", "CRITICAL"]:
            return {
                "warning_id": f"warn-{int(datetime.now().timestamp())}",
                "level": WarningLevel.WARNING,
                "message": f"High probability of {forecast.event_type} at {forecast.location}",
                "forecast_reference": forecast.model_dump()
            }
            
        elif forecast.probability > 0.50:
             return {
                "warning_id": f"warn-{int(datetime.now().timestamp())}",
                "level": WarningLevel.WATCH,
                "message": f"Monitoring potential {forecast.event_type} at {forecast.location}",
                "forecast_reference": forecast.model_dump()
            }
            
        return None
