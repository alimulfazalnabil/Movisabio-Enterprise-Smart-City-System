class FallbackManager:
    """
    Triggers physical controllers to revert to default timing plans if MoviSabio fails.
    """
    def __init__(self, controller_protocol):
        self.controller = controller_protocol
        self.is_active = False
        
    def trigger_fallback(self, reason: str):
        """
        Disables AI control. The physical controller resumes its fixed-time 
        or actuated baseline program.
        """
        print(f"[FALLBACK] Triggered. Reason: {reason}")
        self.is_active = True
        return self.controller.disable_ai_control()
        
    def resolve_fallback(self) -> bool:
        """
        Operator re-enables AI control manually.
        """
        self.is_active = False
        return self.controller.enable_ai_control()
