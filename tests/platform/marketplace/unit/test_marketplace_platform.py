from src.platform.marketplace.catalog.product import ProductCatalog, MarketplaceProduct, ProductType, ProductState
from src.platform.marketplace.discovery.search import MarketplaceSearch
from src.platform.marketplace.installation.installer import InstallationManager, MarketplaceInstallation, InstallationState
from src.platform.marketplace.subscriptions.manager import SubscriptionManager, MarketplaceSubscription, SubscriptionState
from src.platform.marketplace.revenue.share import RevenueEngine, RevenueShareRule
from datetime import datetime, timedelta, timezone

def test_catalog_and_search():
    catalog = ProductCatalog()
    
    p1 = MarketplaceProduct(
        product_id="p-1", 
        publisher_id="pub-1", 
        name="Flood Predictor", 
        product_type=ProductType.APPLICATION,
        category="Environment",
        regions=["GLOBAL"]
    )
    catalog.register_product(p1)
    catalog.update_state("p-1", ProductState.PUBLISHED)
    
    p2 = MarketplaceProduct(
        product_id="p-2", 
        publisher_id="pub-2", 
        name="Traffic Analyzer", 
        product_type=ProductType.APPLICATION,
        category="Mobility",
        regions=["Europe"]
    )
    catalog.register_product(p2)
    catalog.update_state("p-2", ProductState.PUBLISHED)
    
    search = MarketplaceSearch(catalog)
    
    # Search by category
    res = search.search(category="Environment")
    assert len(res) == 1
    assert res[0].name == "Flood Predictor"
    
    # Search by region
    res = search.search(region="Europe")
    # p1 is GLOBAL, p2 is Europe, so both should match if looking in Europe
    # Wait, the rule says: region not in product.regions and "GLOBAL" not in product.regions
    assert len(res) == 2

def test_installation_manager():
    installer = InstallationManager()
    inst = MarketplaceInstallation(
        installation_id="inst-1",
        tenant_id="t-1",
        product_id="p-1",
        region="Europe"
    )
    installer.start_installation(inst)
    assert installer.installations["inst-1"].state == InstallationState.PENDING
    installer.update_state("inst-1", InstallationState.ACTIVE)
    assert installer.installations["inst-1"].state == InstallationState.ACTIVE

def test_subscription_manager():
    sm = SubscriptionManager()
    sub = MarketplaceSubscription(
        subscription_id="sub-1",
        tenant_id="t-1",
        product_id="p-1",
        plan_name="Enterprise",
        expires_at=datetime.now(timezone.utc) + timedelta(days=30)
    )
    sm.create_subscription(sub)
    assert sm.subscriptions["sub-1"].state == SubscriptionState.ACTIVE
    
    sm.renew("sub-1", datetime.now(timezone.utc) + timedelta(days=60))
    assert sm.subscriptions["sub-1"].state == SubscriptionState.ACTIVE

def test_revenue_share():
    engine = RevenueEngine()
    rule = RevenueShareRule(
        product_id="p-1",
        developer_percentage=80.0,
        platform_percentage=20.0
    )
    engine.set_rule(rule)
    
    payout = engine.process_payment("p-1", 100.0, "USD", "dev-1")
    assert payout.amount == 80.0
    assert len(engine.payouts) == 1
