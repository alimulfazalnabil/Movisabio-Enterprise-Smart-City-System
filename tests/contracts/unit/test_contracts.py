from datetime import datetime, timezone
from packages.contracts.events.envelope import EventEnvelope, EventSource
from packages.contracts.entities.envelope import EntityEnvelope, EntitySource
from packages.contracts.observations.envelope import ObservationEnvelope, ObservationSource
from packages.contracts.decisions.envelope import DecisionEnvelope, SafetyValidation, AuthorizationStatus, ExecutionStatus
from packages.contracts.commands.envelope import CommandEnvelope

def test_event_envelope():
    ev = EventEnvelope(
        event_id="evt_123",
        event_type="FloodDetected",
        occurred_at=datetime.now(timezone.utc),
        published_at=datetime.now(timezone.utc),
        tenant_id="tenant_001",
        organization_id="org_001",
        source=EventSource(service="flood-intelligence", instance="worker-1"),
        correlation_id="corr_123",
        payload={"level_m": 2.5}
    )
    assert ev.event_id == "evt_123"
    assert ev.payload["level_m"] == 2.5

def test_entity_envelope():
    ent = EntityEnvelope(
        entity_id="ent_123",
        entity_type="HOSPITAL",
        tenant_id="tenant_001",
        status="ACTIVE",
        valid_from=datetime.now(timezone.utc),
        source=EntitySource(type="OFFICIAL", id="registry_123"),
        data_quality="VALID"
    )
    assert ent.entity_id == "ent_123"

def test_observation_envelope():
    obs = ObservationEnvelope(
        observation_id="obs_123",
        subject_id="asset_123",
        observation_type="TEMPERATURE",
        observed_at=datetime.now(timezone.utc),
        value=31.4,
        unit="CELSIUS",
        source=ObservationSource(device_id="sensor_123"),
        quality="VALID",
        confidence=0.98
    )
    assert obs.observation_id == "obs_123"

def test_decision_envelope():
    dec = DecisionEnvelope(
        decision_id="dec_123",
        decision_type="TRAFFIC_SIGNAL_OPTIMIZATION",
        subject_id="intersection_123",
        agent_id="traffic-agent",
        model_version="ppo-v14",
        confidence=0.91,
        policy_version="policy-7",
        safety_validation=SafetyValidation(status="PASSED"),
        authorization=AuthorizationStatus(status="AUTHORIZED"),
        execution=ExecutionStatus(status="PENDING")
    )
    assert dec.decision_id == "dec_123"

def test_command_envelope():
    cmd = CommandEnvelope(
        command_id="cmd_123",
        target_type="TRAFFIC_CONTROLLER",
        target_id="controller_123",
        command_type="SET_SIGNAL_PHASE",
        requested_by="traffic-agent",
        policy_version="policy-7",
        safety_policy_version="safety-4",
        idempotency_key="idem_123",
        expires_at=datetime.now(timezone.utc)
    )
    assert cmd.command_id == "cmd_123"
