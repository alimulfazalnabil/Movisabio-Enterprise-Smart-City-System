from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class TicketPriority(str, enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"

class TicketStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVING = "RESOLVING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class SupportTicket(BaseModel):
    ticket_id: str
    customer_id: str
    priority: TicketPriority
    status: TicketStatus = TicketStatus.SUBMITTED
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SupportEngine:
    def __init__(self):
        self.tickets: Dict[str, SupportTicket] = {}
        
    def create_ticket(self, ticket: SupportTicket) -> SupportTicket:
        self.tickets[ticket.ticket_id] = ticket
        return ticket
        
    def update_status(self, ticket_id: str, new_status: TicketStatus) -> SupportTicket:
        if ticket_id not in self.tickets:
            raise ValueError("Ticket not found")
        self.tickets[ticket_id].status = new_status
        return self.tickets[ticket_id]
