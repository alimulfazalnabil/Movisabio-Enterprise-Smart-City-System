from src.platform.solution_delivery.requirements.requirement import RequirementsEngine, ProjectRequirement, RequirementCategory, RequirementStatus
from src.platform.solution_delivery.architecture.adr import ArchitectureEngine, ArchitectureDecisionRecord, ADRStatus
from src.platform.solution_delivery.site_surveys.survey import SurveyEngine, SiteSurvey, SurveyStatus
from src.platform.solution_delivery.implementation.project import DeliveryEngine, DeliveryProject, ImplementationPhase
from src.platform.solution_delivery.commissioning.commission import CommissioningEngine, CommissioningRecord, CommissioningStatus
from src.platform.solution_delivery.financials.costing import FinancialEngine

def test_requirements_and_adr():
    req_engine = RequirementsEngine()
    req = ProjectRequirement(
        requirement_id="req-1",
        project_id="p-1",
        title="Detect queues",
        description="Detect queues",
        category=RequirementCategory.FUNCTIONAL
    )
    req_engine.add_requirement(req)
    req_engine.update_status("req-1", RequirementStatus.APPROVED)
    assert req_engine.requirements["req-1"].status == RequirementStatus.APPROVED
    
    arch_engine = ArchitectureEngine()
    adr = ArchitectureDecisionRecord(
        adr_id="adr-1",
        project_id="p-1",
        title="Edge inference",
        context="Need low latency",
        decision="Use edge CV",
        alternatives_considered=["Cloud CV"],
        consequences="Requires edge compute"
    )
    arch_engine.submit_adr(adr)
    arch_engine.approve_adr("adr-1", "architect-1")
    assert arch_engine.adrs["adr-1"].status == ADRStatus.ACCEPTED

def test_survey_and_commissioning():
    survey_engine = SurveyEngine()
    survey = SiteSurvey(
        survey_id="s-1",
        project_id="p-1",
        site_id="site-1"
    )
    survey_engine.create_survey(survey)
    survey_engine.complete_survey("s-1", {"power": "available"})
    assert survey_engine.surveys["s-1"].status == SurveyStatus.COMPLETED
    
    comm_engine = CommissioningEngine()
    record = CommissioningRecord(
        record_id="c-1",
        project_id="p-1",
        site_id="site-1"
    )
    comm_engine.start_commissioning(record)
    comm_engine.complete_checklist("c-1", {"camera_working": True, "network_working": True}, [])
    assert comm_engine.records["c-1"].status == CommissioningStatus.VALIDATED

def test_delivery_project_and_financials():
    del_engine = DeliveryEngine()
    proj = DeliveryProject(
        project_id="p-1",
        customer_id="cust-1",
        name="Smart Traffic"
    )
    del_engine.create_project(proj)
    del_engine.advance_phase("p-1", ImplementationPhase.DESIGN)
    assert del_engine.projects["p-1"].phase == ImplementationPhase.DESIGN
    
    fin_engine = FinancialEngine()
    fin_engine.initialize_project("p-1", planned_cost=100000, planned_revenue=150000)
    fin_engine.add_cost("p-1", 50000)
    
    fin = fin_engine.financials["p-1"]
    fin.actual_revenue = 150000
    assert fin.gross_margin == ((150000 - 50000) / 150000) * 100
