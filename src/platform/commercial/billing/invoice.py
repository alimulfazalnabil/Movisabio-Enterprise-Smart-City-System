from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, timezone

class InvoiceLine(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_id: str
    tenant_id: str
    period_start: datetime
    period_end: datetime
    currency: str
    lines: List[InvoiceLine]
    total: float = 0.0
    status: str = "DRAFT"

class BillingEngine:
    def __init__(self):
        self.invoices: Dict[str, Invoice] = {}
        
    def generate_invoice(self, tenant_id: str, usage_records: List[Dict], pricing_catalog: Dict[str, float]) -> Invoice:
        invoice_id = f"inv-{len(self.invoices) + 1}"
        lines = []
        total = 0.0
        
        for record in usage_records:
            meter = record["meter"]
            qty = record["quantity"]
            price = pricing_catalog.get(meter, 0.0)
            
            line_total = qty * price
            lines.append(InvoiceLine(
                description=f"Usage for {meter}",
                quantity=qty,
                unit_price=price,
                total=line_total
            ))
            total += line_total
            
        now = datetime.now(timezone.utc)
        
        inv = Invoice(
            invoice_id=invoice_id,
            tenant_id=tenant_id,
            period_start=now,
            period_end=now,
            currency="EUR",
            lines=lines,
            total=total
        )
        self.invoices[invoice_id] = inv
        return inv
        
    def finalize_invoice(self, invoice_id: str) -> None:
        if invoice_id in self.invoices:
            self.invoices[invoice_id].status = "FINALIZED"
