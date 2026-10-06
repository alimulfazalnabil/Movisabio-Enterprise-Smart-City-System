from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class RevenueShareRule(BaseModel):
    product_id: str
    developer_percentage: float
    platform_percentage: float
    partner_percentage: float = 0.0

class PayoutRecord(BaseModel):
    payout_id: str
    product_id: str
    amount: float
    currency: str
    recipient_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RevenueEngine:
    def __init__(self):
        self.rules: Dict[str, RevenueShareRule] = {}
        self.payouts: List[PayoutRecord] = []
        
    def set_rule(self, rule: RevenueShareRule):
        if rule.developer_percentage + rule.platform_percentage + rule.partner_percentage != 100.0:
            raise ValueError("Percentages must sum to 100")
        self.rules[rule.product_id] = rule
        
    def process_payment(self, product_id: str, amount: float, currency: str, dev_id: str):
        if product_id not in self.rules:
            raise ValueError("No revenue share rule found for product")
            
        rule = self.rules[product_id]
        dev_amount = amount * (rule.developer_percentage / 100.0)
        
        payout = PayoutRecord(
            payout_id=f"pay-{len(self.payouts)+1}",
            product_id=product_id,
            amount=dev_amount,
            currency=currency,
            recipient_id=dev_id
        )
        self.payouts.append(payout)
        return payout
