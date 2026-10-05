from src.services.finance.models.schemas import ProjectFinancialModel, FinancialMetrics

class ProjectFinanceEngine:
    def calculate_metrics(self, model: ProjectFinancialModel) -> FinancialMetrics:
        """
        Calculates financial metrics (e.g. Cash Flow) for a project.
        """
        # Cash Flow = Revenue - OPEX - Maintenance - Financing Costs
        cash_flow = model.revenue - model.opex - model.maintenance - model.financing_costs
        
        # Simple payback period (assuming linear cash flow, ignoring time value of money for this example)
        payback_period = None
        if cash_flow > 0:
            payback_period = model.capex / cash_flow
            
        return FinancialMetrics(
            project_id=model.project_id,
            cash_flow=cash_flow,
            payback_period=payback_period
        )
