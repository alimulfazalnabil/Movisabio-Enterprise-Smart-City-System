from abc import ABC, abstractmethod
from typing import AsyncGenerator
from src.packages.events.schemas import CanonicalEvent

class DataSourceAdapter(ABC):
    """
    Abstract adapter defining how external data flows into the MoviSabio ingestion pipeline.
    """
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the underlying data source."""
        pass
        
    @abstractmethod
    async def health(self) -> str:
        """Return 'healthy', 'degraded', or 'offline'."""
        pass

    @abstractmethod
    async def receive(self) -> AsyncGenerator[CanonicalEvent, None]:
        """
        Yields normalized CanonicalEvent streams.
        Any raw data parsing must happen internally before yielding.
        """
        yield # type: ignore
        
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connections gracefully."""
        pass
