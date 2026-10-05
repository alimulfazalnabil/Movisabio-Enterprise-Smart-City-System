from src.services.science.models.schemas import Publication, Experiment
from src.services.science.engine.knowledge_graph import KnowledgeGraphEngine
from src.services.science.engine.experiment import ExperimentEngine

def test_knowledge_graph_evidence_filtering():
    pub1 = Publication(publication_id="PUB-1", title="Quantum Traffic Control", authors=["Alice"], citations=[], evidence_level="PRIMARY_RESEARCH")
    pub2 = Publication(publication_id="PUB-2", title="AI Generated Flood Model Hypothesis", authors=["Bob"], citations=["PUB-1"], evidence_level="AI_GENERATED_HYPOTHESIS")
    
    engine = KnowledgeGraphEngine(publications=[pub1, pub2])
    
    # Should only return PRIMARY_RESEARCH
    verified = engine.filter_evidence(["PRIMARY_RESEARCH", "SYSTEMATIC_REVIEW"])
    assert len(verified) == 1
    assert verified[0].publication_id == "PUB-1"

def test_experiment_reproducibility():
    engine = ExperimentEngine()
    
    # Non-reproducible (using LATEST tag)
    exp_invalid = Experiment(
        experiment_id="EXP-1",
        project_id="PROJ-1",
        code_version="LATEST",
        dataset_version="v1.0",
        parameters={"learning_rate": "0.01"},
        status="COMPLETED"
    )
    assert engine.validate_reproducibility(exp_invalid) is False
    
    # Reproducible (explicit hashes/tags)
    exp_valid = Experiment(
        experiment_id="EXP-2",
        project_id="PROJ-1",
        code_version="ab12cd34",
        dataset_version="v2.1",
        parameters={"learning_rate": "0.01"},
        status="COMPLETED"
    )
    assert engine.validate_reproducibility(exp_valid) is True
