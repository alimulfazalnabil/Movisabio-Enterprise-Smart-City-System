from datetime import datetime, timezone
from src.platform.commercial.tenant.registry import TenantRegistry, Organization, Tenant
from src.platform.commercial.subscription.entitlement import EntitlementEngine, Subscription, Entitlement
from src.platform.commercial.billing.invoice import BillingEngine

def test_tenant_registry():
    reg = TenantRegistry()
    org = Organization(org_id="org-1", name="City of Munich", customer_type="MUNICIPALITY", created_at=datetime.now(timezone.utc))
    reg.register_organization(org)
    
    tenant = Tenant(tenant_id="tenant-1", org_id="org-1", name="Munich Traffic", region_id="eu-de-01", created_at=datetime.now(timezone.utc))
    reg.register_tenant(tenant)
    
    assert reg.get_tenant("tenant-1").name == "Munich Traffic"

def test_entitlement_engine():
    engine = EntitlementEngine()
    
    sub = Subscription(
        subscription_id="sub-1",
        tenant_id="tenant-1",
        plan_id="enterprise",
        entitlements={
            "cameras": Entitlement(entitlement_id="e1", feature_code="cameras", limit_type="QUANTITY", limit_value=100),
            "digital_twin": Entitlement(entitlement_id="e2", feature_code="digital_twin", limit_type="BOOLEAN")
        }
    )
    engine.add_subscription(sub)
    
    # Check boolean
    assert engine.check_entitlement("tenant-1", "digital_twin") is True
    
    # Check quantity consumption
    assert engine.consume("tenant-1", "cameras", 50) is True
    assert engine.consume("tenant-1", "cameras", 60) is False # Would exceed 100 limit
    
    assert engine.subscriptions["tenant-1"].entitlements["cameras"].consumed_value == 50.0

def test_billing_engine():
    engine = BillingEngine()
    
    usage_records = [
        {"meter": "traffic.camera_processing", "quantity": 500},
        {"meter": "api_calls", "quantity": 2500}
    ]
    
    pricing = {
        "traffic.camera_processing": 10.0,
        "api_calls": 0.01
    }
    
    inv = engine.generate_invoice("tenant-1", usage_records, pricing)
    
    assert inv.status == "DRAFT"
    assert inv.total == 500 * 10.0 + 2500 * 0.01
    
    engine.finalize_invoice(inv.invoice_id)
    assert engine.invoices[inv.invoice_id].status == "FINALIZED"
