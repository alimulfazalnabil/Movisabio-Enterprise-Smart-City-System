from src.platform.service_management.support.ticket import SupportEngine, SupportTicket, TicketPriority, TicketStatus
from src.platform.service_management.sla.monitor import SLAMonitor, SLABreachStatus
from typing import Optional

def test_support_engine():
    engine = SupportEngine()
    ticket = SupportTicket(
        ticket_id="t-1",
        customer_id="cust-1",
        priority=TicketPriority.P1,
        title="System down",
        description="Help"
    )
    engine.create_ticket(ticket)
    assert engine.tickets["t-1"].status == TicketStatus.SUBMITTED
    engine.update_status("t-1", TicketStatus.RESOLVED)
    assert engine.tickets["t-1"].status == TicketStatus.RESOLVED

def test_sla_monitor():
    monitor = SLAMonitor()
    breach = monitor.record_measurement("b-1", "cust-1", "API Latency", target=100.0, actual=150.0)
    assert breach is not None
    assert breach.status == SLABreachStatus.BREACH_CANDIDATE
    
    validated = monitor.validate_breach("b-1")
    assert validated.status == SLABreachStatus.VALIDATED
    
    # Not a breach
    no_breach = monitor.record_measurement("b-2", "cust-1", "API Latency", target=100.0, actual=50.0)
    assert no_breach is None
