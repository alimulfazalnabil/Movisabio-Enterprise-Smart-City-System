from src.platform.knowledge.query.plan import QueryPlanner, QueryPlan, QueryEntity, SpatialConstraint
from src.platform.knowledge.provenance.claim import KnowledgeClaim, ProvenanceEngine, EvidenceTier
from src.platform.knowledge.search.hybrid import HybridSearchRouter
from src.platform.knowledge.rag.engine import RAGEngine

def test_query_plan_validation():
    planner = QueryPlanner()
    plan = QueryPlan(
        query_id="q1",
        intent="spatial_analysis",
        entities=[QueryEntity(type="HOSPITAL", scope="city-1")],
        spatial=SpatialConstraint(relation="NEAR", distance_meters=500, target_entity="FLOOD_ZONE")
    )
    assert planner.validate_plan(plan) is True

def test_provenance_verification():
    engine = ProvenanceEngine()
    
    strong_claim = KnowledgeClaim(
        claim_id="c1",
        subject_id="road-1",
        predicate="HAS_STATUS",
        object_value="CLOSED",
        confidence=0.99,
        evidence_tier=EvidenceTier.AUTHORITATIVE_RECORD,
        sources=["police-db"]
    )
    
    weak_claim = KnowledgeClaim(
        claim_id="c2",
        subject_id="road-1",
        predicate="HAS_CONGESTION",
        object_value="HIGH",
        confidence=0.60,
        evidence_tier=EvidenceTier.AI_INFERENCE,
        sources=["llm-agent"]
    )
    
    # Authoritative record passes Verified Sensor check
    assert engine.verify_claim(strong_claim, EvidenceTier.VERIFIED_SENSOR) is True
    # AI Inference fails Scientific Data check
    assert engine.verify_claim(weak_claim, EvidenceTier.SCIENTIFIC_DATA) is False

def test_hybrid_search():
    router = HybridSearchRouter()
    plan = QueryPlan(
        query_id="q1",
        intent="spatial_analysis",
        entities=[QueryEntity(type="HOSPITAL", scope="city-1")],
        spatial=SpatialConstraint(relation="NEAR", distance_meters=500)
    )
    
    results = router.execute_plan(plan)
    assert len(results) == 2 # Spatial + Semantic fallback
    assert results[0].source_index == "spatial" # Highest relevance in mock

def test_rag_engine():
    prov_engine = ProvenanceEngine()
    rag = RAGEngine(prov_engine)
    
    valid_claim = KnowledgeClaim(
        claim_id="c1",
        subject_id="bridge-1",
        predicate="CONDITION",
        object_value="POOR",
        confidence=0.95,
        evidence_tier=EvidenceTier.VERIFIED_FIELD_OBSERVATION,
        sources=["inspector-app"]
    )
    
    unverified_claim = KnowledgeClaim(
        claim_id="c2",
        subject_id="bridge-1",
        predicate="CAUSE",
        object_value="UNKNOWN_VIBRATION",
        confidence=0.4,
        evidence_tier=EvidenceTier.AI_INFERENCE,
        sources=["llm-guess"]
    )
    
    answer = rag.generate_and_validate_answer(
        query="What is the bridge condition?",
        context_claims=[valid_claim, unverified_claim]
    )
    
    # RAGEngine mock requires VALIDATED_MODEL_OUTPUT or higher
    assert answer.is_hallucination_detected is True
    assert len(answer.claims) == 1
    assert answer.claims[0].claim_id == "c1"
    assert answer.grounding_score == 0.5
