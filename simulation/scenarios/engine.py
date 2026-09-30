import enum
from typing import Dict, Any

class ScenarioType(str, enum.Enum):
    NORMAL = "normal"
    RUSH_HOUR = "rush_hour"
    INCIDENT = "incident"
    RAIN = "rain"
    EVENT = "event"
    ROAD_CLOSURE = "road_closure"
    EMERGENCY_VEHICLE = "emergency_vehicle"

class SUMOScenarioBuilder:
    """
    Phase 4: Digital Twin Configuration
    Builds TraCI / SUMO environments based on standardized scenarios.
    """
    def __init__(self, map_file: str):
        self.map_file = map_file # e.g. imported from OpenStreetMap (.net.xml)

    def generate_scenario(self, scenario_type: ScenarioType) -> Dict[str, Any]:
        """
        Generates the SUMO configuration files and traffic demand profiles for a given scenario.
        """
        base_config = {
            "net-file": self.map_file,
            "route-files": f"routes_{scenario_type.value}.rou.xml",
            "step-length": "0.1",
        }
        
        # Apply modifiers based on scenario
        if scenario_type == ScenarioType.RUSH_HOUR:
            base_config["scale"] = "2.5" # 2.5x traffic density
        elif scenario_type == ScenarioType.RAIN:
            # Global speed modifier for adverse weather
            base_config["step-length"] = "0.2"
            base_config["default.speeddev"] = "0.2"
        elif scenario_type == ScenarioType.EMERGENCY_VEHICLE:
            # Ensure emergency vehicle spawn
            base_config["additional-files"] = "emergency_vtype.add.xml"
            
        return base_config
