from abc import ABC, abstractmethod
from typing import Dict, Any

class SimulationEngineInterface(ABC):
    
    @abstractmethod
    def prepare(self, scenario_config: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def initialize(self, snapshot_data: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def step(self, simulation_time: int) -> None:
        pass
        
    @abstractmethod
    def get_results(self) -> Dict[str, Any]:
        pass

class SUMOEngineAdapter(SimulationEngineInterface):
    def prepare(self, scenario_config: Dict[str, Any]) -> None:
        # Load SUMO config
        pass
        
    def initialize(self, snapshot_data: Dict[str, Any]) -> None:
        # Set initial traffic state via TraCI
        pass
        
    def step(self, simulation_time: int) -> None:
        # traci.simulationStep()
        pass
        
    def get_results(self) -> Dict[str, Any]:
        return {"avg_speed": 35.5, "total_delay": 1200}
