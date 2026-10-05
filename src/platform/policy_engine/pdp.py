from typing import List
from src.platform.access_control.abac import AccessRequest, AuthorizationDecision
from src.platform.identity.models import AIAgentIdentity
from datetime import datetime, timezone, timedelta

class PolicyDecisionPoint:
    def __init__(self, policy_version: str):
        self.policy_version = policy_version
        
    def evaluate(self, request: AccessRequest) -> AuthorizationDecision:
        # Deny if identity is not ACTIVE
        if request.subject.status != "ACTIVE":
            return self._deny(request, "IDENTITY_NOT_ACTIVE")
            
        # Deny cross-tenant access without explicit federation (simplified for now)
        if request.subject.tenant_id and request.subject.tenant_id != request.tenant_id:
            return self._deny(request, "CROSS_TENANT_DENIED")
            
        # AI Agent checks
        if isinstance(request.subject, AIAgentIdentity):
            if request.action in request.subject.forbidden_capabilities:
                return self._deny(request, "AGENT_ACTION_FORBIDDEN")
            if request.action not in request.subject.capabilities:
                return self._deny(request, "AGENT_ACTION_NOT_GRANTED")
                
        # Basic RBAC check
        # For a full implementation, we'd map actions to roles.
        # Here we do a simplified check for physical control vs operational roles
        if "control.execute" in request.action:
            if "operator" not in request.subject.roles and not isinstance(request.subject, AIAgentIdentity):
                return self._deny(request, "MISSING_ROLE_FOR_CONTROL")
                
        # If all checks pass
        return AuthorizationDecision(
            decision="ALLOW",
            subject_id=request.subject.identity_id,
            action=request.action,
            resource_id=request.resource_id,
            tenant_id=request.tenant_id,
            risk_class="R3", # Example dynamic risk assignment
            conditions=["POLICY_CHECKS_PASSED"],
            policy_version=self.policy_version,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)
        )
        
    def _deny(self, request: AccessRequest, reason: str) -> AuthorizationDecision:
        return AuthorizationDecision(
            decision="DENY",
            subject_id=request.subject.identity_id,
            action=request.action,
            resource_id=request.resource_id,
            tenant_id=request.tenant_id,
            conditions=[reason],
            policy_version=self.policy_version
        )
