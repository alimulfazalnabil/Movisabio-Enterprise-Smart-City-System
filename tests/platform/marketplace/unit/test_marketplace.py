from src.platform.marketplace.registry.product import ProductRegistry, MarketplaceProduct, ProductType, ProductStatus
from src.platform.marketplace.governance.lifecycle import ProductGovernanceEngine
from src.platform.marketplace.licensing.license import EntitlementEngine, ProductLicense, UsageRight
from src.platform.marketplace.billing.subscription import SubscriptionManager, Subscription
from src.platform.marketplace.billing.metering import MeteringEngine, UsageRecord

def test_product_registry():
    registry = ProductRegistry()
    prod = MarketplaceProduct(
        product_id="prod-1", tenant_id="t1", product_type=ProductType.DATASET,
        name="Traffic Flow", description="Flow data", owner_id="o1", provider_id="p1"
    )
    registry.register_product(prod)
    assert registry.get_product("prod-1").status == ProductStatus.REGISTERED

def test_governance_engine():
    registry = ProductRegistry()
    registry.register_product(MarketplaceProduct(
        product_id="prod-1", tenant_id="t1", product_type=ProductType.DATASET,
        name="Data", description="D", owner_id="o", provider_id="p"
    ))
    
    gov = ProductGovernanceEngine(registry)
    # Missing commercial check
    approved = gov.approve_for_publication("prod-1", {"OWNERSHIP": True, "LICENSE": True, "PRIVACY": True, "SECURITY": True, "COMMERCIAL": True})
    assert approved is True
    assert registry.get_product("prod-1").status == ProductStatus.PUBLISHED
    
    gov.suspend_product("prod-1", "quality issues")
    assert registry.get_product("prod-1").status == ProductStatus.SUSPENDED

def test_licensing_entitlements():
    engine = EntitlementEngine()
    engine.attach_license(ProductLicense(
        license_id="lic-1", product_id="prod-1",
        allowed_rights=[UsageRight.VIEW, UsageRight.API_ACCESS],
        restricted_rights=[UsageRight.MODEL_TRAINING, UsageRight.COMMERCIALIZE]
    ))
    
    assert engine.verify_entitlement("prod-1", UsageRight.API_ACCESS) is True
    assert engine.verify_entitlement("prod-1", UsageRight.MODEL_TRAINING) is False

def test_billing_and_metering():
    sub_manager = SubscriptionManager()
    sub_manager.create_subscription(Subscription(
        subscription_id="sub-1", tenant_id="t1", product_id="prod-1",
        entitlements={"api_calls": 1000}
    ))
    
    assert sub_manager.check_entitlement("sub-1", "api_calls", 500) is True
    assert sub_manager.check_entitlement("sub-1", "api_calls", 1500) is False
    
    meter = MeteringEngine()
    meter.record_usage(UsageRecord(usage_id="u1", subscription_id="sub-1", metric="api_calls", quantity=100))
    meter.record_usage(UsageRecord(usage_id="u2", subscription_id="sub-1", metric="api_calls", quantity=250))
    
    assert meter.get_total_usage("sub-1", "api_calls") == 350
