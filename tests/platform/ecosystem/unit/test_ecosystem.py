from src.platform.ecosystem.extensions.extension import ExtensionRegistry, EcosystemExtension, ExtensionStatus
from src.platform.ecosystem.partners.partner import PartnerRegistry, EcosystemPartner, PartnerStatus
from src.platform.event_platform.subscriptions.subscription import SubscriptionManager, EventSubscription
from src.platform.event_platform.webhooks.webhook import WebhookManager, Webhook, WebhookStatus
from src.platform.certification.security.validator import SecurityValidator

def test_extension_registry():
    registry = ExtensionRegistry()
    ext = EcosystemExtension(extension_id="ext-1", publisher_id="p1", extension_type="analytics", name="Flow", version="1.0")
    registry.register_extension(ext)
    assert registry.extensions["ext-1"].status == ExtensionStatus.SUBMITTED
    
    registry.certify_extension("ext-1")
    assert registry.extensions["ext-1"].status == ExtensionStatus.CERTIFIED

def test_partner_registry():
    registry = PartnerRegistry()
    partner = EcosystemPartner(partner_id="p-1", name="ACME Corp", partner_type="integration")
    registry.register_partner(partner)
    registry.approve_partner("p-1")
    assert registry.partners["p-1"].status == PartnerStatus.APPROVED

def test_subscriptions():
    manager = SubscriptionManager()
    manager.register_subscription(EventSubscription(
        subscription_id="sub-1", application_id="app-1", event_types=["traffic.congestion"]
    ))
    subs = manager.get_subscriptions_for_event("traffic.congestion")
    assert len(subs) == 1
    assert subs[0].subscription_id == "sub-1"

def test_webhooks():
    manager = WebhookManager()
    manager.register_webhook(Webhook(webhook_id="w-1", application_id="app-1", endpoint_url="https://example.com", secret="123"))
    manager.activate_webhook("w-1")
    assert manager.webhooks["w-1"].status == WebhookStatus.ACTIVE

def test_security_validator():
    validator = SecurityValidator()
    
    # Valid
    assert validator.validate_extension({
        "name": "Test", "version": "1.0", "publisher_id": "p1", "permissions": ["traffic.read"]
    }) is True
    
    # Invalid: physical control not allowed
    assert validator.validate_extension({
        "name": "Test", "version": "1.0", "publisher_id": "p1", "permissions": ["traffic.control"]
    }) is False
