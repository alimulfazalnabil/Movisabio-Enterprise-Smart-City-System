class EventBus:
    """
    Enterprise Event Bus handling thousands of edge and cloud telemetry events.
    In production, this wraps Kafka or RabbitMQ.
    """
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
    def publish(self, event_type: str, payload: dict):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(payload)
                
# Global instance
event_bus = EventBus()
