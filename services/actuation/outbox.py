import uuid
import datetime
from pydantic import BaseModel
from typing import Protocol, Optional

class TrafficSignalController(Protocol):
    async def get_status(self) -> dict:
        ...

    async def apply_command(self, command: 'OutboxCommand') -> bool:
        ...

    async def emergency_preemption(self, phase: str) -> bool:
        ...

    async def fail_safe(self) -> bool:
        ...

class OutboxCommand(BaseModel):
    command_id: str
    intersection_id: str
    phase: str
    requested_state: str
    requested_at: datetime.datetime
    status: str # PENDING, SENT, ACK, NACK
    reason: str

class CommandOutbox:
    """
    Never send commands directly from the AI engine.
    Decision -> Safety -> Command -> PostgreSQL Outbox -> Broker -> Controller
    """
    def __init__(self):
        # Mocks a database table for outbox
        self.outbox_store = {}
        
    def create_command(self, intersection_id: str, phase: str, requested_state: str, reason: str) -> OutboxCommand:
        cmd = OutboxCommand(
            command_id=str(uuid.uuid4()),
            intersection_id=intersection_id,
            phase=phase,
            requested_state=requested_state,
            requested_at=datetime.datetime.now(datetime.timezone.utc),
            status="PENDING",
            reason=reason
        )
        self.outbox_store[cmd.command_id] = cmd
        return cmd
        
    def mark_sent(self, command_id: str):
        if command_id in self.outbox_store:
            self.outbox_store[command_id].status = "SENT"

    def mark_ack(self, command_id: str):
        if command_id in self.outbox_store:
            self.outbox_store[command_id].status = "ACK"
