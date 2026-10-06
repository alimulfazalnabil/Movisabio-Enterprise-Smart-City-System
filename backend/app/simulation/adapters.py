from abc import ABC, abstractmethod

class SimulationAdapter(ABC):
    @abstractmethod
    def start_simulation(self):
        pass
        
    @abstractmethod
    def get_vehicle_state(self) -> dict:
        pass
        
    @abstractmethod
    def set_signal_state(self, intersection_id: str, phase: str, duration: float):
        pass

class SUMOAdapter(SimulationAdapter):
    def __init__(self, config_path: str):
        self.config_path = config_path
        
    def start_simulation(self):
        # mock traci.start(["sumo", "-c", self.config_path])
        pass
        
    def get_vehicle_state(self) -> dict:
        return {}
        
    def set_signal_state(self, intersection_id: str, phase: str, duration: float):
        pass
