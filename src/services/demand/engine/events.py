from typing import List
from src.services.demand.models.schemas import EventDemand, MobilityDemand

class EventMobilityForecaster:
    """
    Translates territorial events into mobility demand loads.
    """
    
    def generate_event_demand(self, event: EventDemand) -> List[MobilityDemand]:
        """
        Creates MobilityDemand records based on event expected attendance and mode split.
        """
        demands = []
        
        # Simplified: all attendees arrive via the specified modes
        for mode, percentage in event.mode_split.items():
            volume = int(event.expected_attendance * percentage)
            
            # Assume 80% arrive in the hour before the event
            arrival_volume = int(volume * 0.8)
            
            demands.append(MobilityDemand(
                origin_zone="EXTERNAL", # Simplified catch-all for event generation
                destination_zone=event.location_zone,
                time_window_start=event.start_time,
                time_window_end=event.end_time,
                mode=mode,
                trip_purpose="EVENT",
                volume_estimate=arrival_volume,
                confidence=0.75
            ))
            
        return demands
