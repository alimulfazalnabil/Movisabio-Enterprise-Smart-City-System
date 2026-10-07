from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class QuantumWorkload(Base):
    """B42.3 - Quantum Workload Registry"""
    __tablename__ = "quantum_workloads"
    workload_id = Column(String, primary_key=True)
    domain = Column(String) # e.g. "mobility.traffic_optimization"
    classification = Column(String) # C0, C1, Q1, Q2, Q3
    evidence_status = Column(String) # CONCEPTUAL, SIMULATED, EXPERIMENTAL, BENCHMARKED, ADVANTAGE
    classical_baseline = Column(JSON)
    quantum_formulation = Column(String) # QUBO, QAOA, VQE, etc.
    is_active = Column(Boolean, default=True)

class QuantumBenchmark(Base):
    """B42.11 - Quantum Benchmarking"""
    __tablename__ = "quantum_benchmarks"
    benchmark_id = Column(String, primary_key=True)
    workload_id = Column(String, ForeignKey("quantum_workloads.workload_id"))
    problem_size = Column(Integer)
    classical_solver = Column(String)
    classical_runtime_ms = Column(Float)
    classical_quality = Column(Float)
    quantum_backend = Column(String) # Simulator or Hardware
    quantum_runtime_ms = Column(Float)
    quantum_quality = Column(Float)
    advantage_demonstrated = Column(Boolean)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class QuantumReadinessIndex(Base):
    """B42.26 - Territorial Quantum Readiness Index"""
    __tablename__ = "quantum_readiness_index"
    territory_id = Column(String, primary_key=True)
    overall_score = Column(Float)
    research_capacity = Column(Float)
    infrastructure_readiness = Column(Float)
    pqc_migration_status = Column(Float)
    industry_adoption = Column(Float)
    last_assessed = Column(DateTime, default=lambda: datetime.now(timezone.utc))
