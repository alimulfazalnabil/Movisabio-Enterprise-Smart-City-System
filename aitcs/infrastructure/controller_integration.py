"""Process-local controller registry and simulated command acknowledgements."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger("aitcs.infrastructure.controller")

@dataclass(frozen=True)
class ControllerAcknowledgement:
    """Result of attempting to deliver one controller command."""

    intersection_id: str
    command_id: str
    status: str
    error_message: Optional[str]
    latency_ms: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ControllerHealthStatus:
    """Registration metadata and last known heartbeat for a controller."""

    intersection_id: str
    is_online: bool
    last_heartbeat: datetime
    protocol: str
    firmware_version: str

class TrafficControllerIntegrationEngine:
    """Track registered controllers and emulate asynchronous delivery.

    No MQTT, NTCIP or REST transport is used yet; successful delivery is a short
    local delay followed by an acknowledgement.
    """

    def __init__(self, heartbeat_timeout_seconds: float = 15.0):
        """Create an empty registry and store the intended heartbeat timeout."""

        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds
        self.controller_registry: Dict[str, ControllerHealthStatus] = {}

    async def register_controller(self, intersection_id: str, protocol: str, firmware: str) -> None:
        """Register a controller as online in the process-local registry."""
        self.controller_registry[intersection_id] = ControllerHealthStatus(
            intersection_id=intersection_id, is_online=True,
            last_heartbeat=datetime.utcnow(), protocol=protocol, firmware_version=firmware
        )

    async def send_command_to_controller(
        self, intersection_id: str, command_id: str, sanitized_command: Dict[str, Any], protocol: str = "MQTT"
    ) -> ControllerAcknowledgement:
        """Return a simulated ACK for a registered controller, otherwise a NACK.

        ``sanitized_command`` and ``protocol`` are accepted for the future
        transport adapter but are not inspected by the current implementation.
        """
        start_time = asyncio.get_event_loop().time()
        if intersection_id not in self.controller_registry or not self.controller_registry[intersection_id].is_online:
            return ControllerAcknowledgement(intersection_id, command_id, "NACK", "Controller offline or unregistered.", 0.0)
        
        await asyncio.sleep(0.01)
        latency = (asyncio.get_event_loop().time() - start_time) * 1000.0
        return ControllerAcknowledgement(intersection_id, command_id, "ACK", None, round(latency, 2))
