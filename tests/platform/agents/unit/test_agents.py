from datetime import datetime, timezone
from src.platform.agents.registry.agent import Agent, RiskClass, AutonomyMode, AutonomyBudget
from src.platform.agents.tools.gateway import ToolGateway, ToolDefinition
from src.platform.agents.context.snapshot import ContextEngine
from src.platform.agents.orchestration.coordinator import Coordinator, AgentMessage

def test_agent_registry_and_risk():
    agent = Agent(
        agent_id="traffic-agent",
        tenant_id="t1",
        name="Traffic Optimizer",
        domain="traffic",
        risk_class=RiskClass.R3,
        autonomy_mode=AutonomyMode.AUTHORIZED_AUTONOMY,
        autonomy_budget=AutonomyBudget(actions_per_hour=20, max_risk=RiskClass.R3, max_duration_minutes=30),
        permissions=["traffic.simulate", "traffic.recommend"],
        allowed_tools=["tool_simulate", "tool_recommend"]
    )
    
    assert agent.can_execute_action(RiskClass.R2) is True
    assert agent.can_execute_action(RiskClass.R3) is True
    assert agent.can_execute_action(RiskClass.R4) is False # Exceeds budget
    
    # Failsafe overrides
    agent.autonomy_mode = AutonomyMode.FAILSAFE
    assert agent.can_execute_action(RiskClass.R0) is False

def test_tool_gateway():
    agent = Agent(
        agent_id="traffic-agent",
        tenant_id="t1",
        name="Traffic Optimizer",
        domain="traffic",
        risk_class=RiskClass.R3,
        autonomy_mode=AutonomyMode.AUTHORIZED_AUTONOMY,
        autonomy_budget=AutonomyBudget(actions_per_hour=20, max_risk=RiskClass.R3, max_duration_minutes=30),
        permissions=["traffic.simulate", "traffic.recommend"],
        allowed_tools=["tool_simulate", "tool_recommend"]
    )
    
    gateway = ToolGateway()
    
    # Register a valid tool
    gateway.register_tool(ToolDefinition(
        tool_id="tool_recommend",
        risk_level=RiskClass.R3,
        required_permissions=["traffic.recommend"]
    ))
    
    # Register an unauthorized tool
    gateway.register_tool(ToolDefinition(
        tool_id="tool_change_signal",
        risk_level=RiskClass.R5,
        required_permissions=["traffic.controller.direct_write"]
    ))
    
    # Evaluate
    assert gateway.evaluate_invocation(agent, "tool_recommend") is True
    assert gateway.evaluate_invocation(agent, "tool_change_signal") is False

def test_context_engine():
    engine = ContextEngine()
    snapshot = engine.build_snapshot("tenant-001", "city-1", datetime.now(timezone.utc))
    assert snapshot.tenant_id == "tenant-001"
    assert snapshot.data_quality == "VALID"

def test_coordinator_conflict_resolution():
    coordinator = Coordinator()
    
    proposals = [
        {"agent_id": "traffic_agent", "action": "extend_green"},
        {"agent_id": "emergency_agent", "action": "preempt_signal"}
    ]
    
    winner = coordinator.resolve_conflict(proposals)
    assert winner is not None
    assert winner["agent_id"] == "emergency_agent"
