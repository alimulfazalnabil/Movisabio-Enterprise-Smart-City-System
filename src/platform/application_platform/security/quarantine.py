from typing import Dict, Any, List
from src.platform.application_platform.runtime.container import RuntimeEngine, RuntimeStatus

class ApplicationQuarantine:
    def __init__(self, runtime_engine: RuntimeEngine):
        self.runtime_engine = runtime_engine
        self.quarantined_apps: set[str] = set()
        
    def kill_switch(self, application_id: str, reason: str):
        """
        Emergency kill switch for an application.
        """
        self.quarantined_apps.add(application_id)
        # Find all runtimes for this app and stop them
        for runtime_id, runtime in self.runtime_engine.runtimes.items():
            if runtime.application_id == application_id:
                self.runtime_engine.update_status(runtime_id, RuntimeStatus.SUSPENDED)
                
    def is_quarantined(self, application_id: str) -> bool:
        return application_id in self.quarantined_apps
