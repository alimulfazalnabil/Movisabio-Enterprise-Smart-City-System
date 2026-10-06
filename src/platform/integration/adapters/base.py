from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass
        
    @abstractmethod
    def authenticate(self) -> bool:
        pass
        
    @abstractmethod
    def fetch(self, query: Dict[str, Any]) -> Any:
        pass
        
    @abstractmethod
    def normalize(self, raw_data: Any) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def health(self) -> str:
        """Returns HEALTHY, DEGRADED, STALE, FAILED"""
        pass
