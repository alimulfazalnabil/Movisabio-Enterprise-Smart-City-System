from abc import ABC, abstractmethod
from typing import Dict, Any

class DataConnector(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def ingest(self) -> Any:
        pass

    @abstractmethod
    async def validate(self, record: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def normalize(self, record: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def publish(self, event: Dict[str, Any]) -> None:
        pass
