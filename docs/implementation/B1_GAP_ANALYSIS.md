# B1 — Repository Audit & Architecture Gap Matrix

## 1. Executive Summary

This document represents the definitive **B1 Repository Audit** against the frozen MoviSabio A4.37 Architecture. 

**Conclusion:** The repository contains a highly developed **logical domain model** (Python Pydantic schemas, isolated domain stubs, `main.py` pipeline mocks, Streamlit dashboard mocks, and hundreds of passing unit tests). It successfully demonstrates the architectural relationships across domains. 

However, it lacks the **production engineering scaffolding** necessary to run as a live, cyber-physical platform (e.g., FastAPIs, PostGIS databases, Docker, live CV models, Kafka, UI). The system currently relies on in-memory mocks (`MockYOLOTracker`, `MockLaneManager`, etc.).

---

## 2. B1.1 — Repository Inventory

### Actual Structure
```
Movisabio-Enterprise-Smart-City-System-main
├── apps/               # Mock/dummy Streamlit scripts
├── backend/            # Empty / not present
├── frontend/           # Empty / not present
├── services/           # Empty / not present
├── domain/             # Extensive Python logical modeling (50+ domains)
├── platform/           # Governance, Safety, AI oversight modules
├── simulation/         # Unit tests/logic stubs
├── schemas/            # Schemas for mock testing
├── scripts/            # Run scripts (run_sprint_1.py, etc.)
├── tests/              # Extensive pytest suite (passing)
├── docs/               # Architecture docs (A1-A4)
├── requirements.txt    # Basic dependencies
├── pyproject.toml      # Project configuration
├── Dockerfile          # Basic/stub dockerfile
└── docker-compose.yml  # Basic/stub configuration
```

---

## 3. B1.2 — Dependency Audit

| Dependency | Status | Classification |
|---|---|---|
| Python | 3.13 | REQUIRED |
| FastAPI | `requirements.txt` | UNUSED (Not implemented in code yet) |
| SQLAlchemy/GeoAlchemy2| `requirements.txt` | UNUSED |
| OpenCV/YOLO/Torch | `requirements.txt` | UNUSED (CV is mocked) |
| Redis | `requirements.txt` | UNUSED |
| SUMO/TraCI | Missing | MISSING (Needs system installation) |
| React/Node | Missing | MISSING |
| Streamlit | `app.py` script | OPTIONAL (Used for mock UI) |

---

## 4. B1.3 — Traffic Pipeline Audit

| Component | Exists | Functional | Production Ready |
|---|---|---|---|
| Video ingestion | Mocked | No | No |
| YOLO | Mocked | No | No |
| Tracking | Mocked | No | No |
| Lane detection | Mocked | No | No |
| Lane counting | Mocked | No | No |
| Speed estimation | Mocked | No | No |
| Traffic state | Pydantic Schemas | Mocked | No |
| Prediction | Schemas only | No | No |
| SUMO | No | No | No |
| RL | No | No | No |
| Safety engine | Yes (`SafetyEngine`) | Unit Tested | Yes (Needs DB) |
| Signal controller | Mocked | No | No |
| Verification | Mocked | No | No |

---

## 5. B1.4 — Physical Control Audit

Currently, the repository only produces:
```text
Recommended Signal:
NS Green 35s
```
This is **analytics/optimization**, not physical signal control. There is no controller interface, no TraCI loop, and no physical HIL (Hardware-in-the-Loop) bridge.

---

## 6. B1.5 — Database Audit

- **PostgreSQL / PostGIS:** Missing.
- **SQLAlchemy / Alembic:** Missing implementation (only in `requirements.txt`).
- **Migrations:** Missing.
- **Persistent Trace:** Fails requirement. All actions (like `ActionLedger`) are stored in Python dictionaries and lost on restart.

---

## 7. B1.6 — API Audit

**Endpoints:** 0 actual endpoints. `FastAPI` is not utilized in any `main.py` or `src/` code. No OpenAPI spec is generated.

---

## 8. B1.7 — Computer Vision Audit

- **Detection:** Missing (Mocked via `MockYOLOTracker`).
- **Tracking:** Missing.
- **Lane logic:** Missing mathematical polygon logic.
- **Speed:** Missing homography / perspective transformation.

---

## 9. B1.8 — AI/ML Audit

All models are currently **STUBBED/MOCKED**. No weights, training scripts, or ML flow registries exist.

---

## 10. B1.9 — SUMO Audit

- **Files (`.net.xml`, `.rou.xml`, `.sumocfg`):** Missing.
- **TraCI Integration:** Missing.

---

## 11. B1.10 — Safety Audit

The `SafetyEngine` component *does* exist conceptually and enforces minimum green, maximum green, etc. However, because it is not connected to a physical pipeline or real database, its enforcement is purely theoretical via passing unit tests.

---

## 12. B1.11 — Security Audit

- **Auth:** Missing (Mock JWT/OAuth).
- **Secrets:** Mocked.
- **Risk:** High risk if deployed as-is, as there is no real Authentication middleware implemented. 

---

## 13. B1.12 — Deployment Audit

- **Docker:** `Dockerfile` and `docker-compose.yml` exist but appear to be stubs or basic setups.
- **Azure:** No Azure-specific dependencies found. Deployment remains portable.

---

## 14. B1.13 — Testing Audit

- **Unit:** Extensive and passing (`tests/`).
- **Integration:** Missing.
- **E2E / Simulation:** Missing.

---

## 15. B1.14 — Technical Debt

- **Critical:** Missing actual data persistence (SQLAlchemy). Missing API layer (FastAPI).
- **High:** CV pipeline is entirely mocked. Simulation is completely missing.

---

## 16. B1.15 — Final Gap Matrix

| Area | Current Implementation | Target Architecture | Gap | Risk | Priority | Recommended Action |
|---|---|---|---|---|---|---|
| **API** | None | Versioned FastAPI | Complete | High | P0 | Implement FastAPI |
| **DB** | Dicts | PostGIS + tenancy | Complete | High | P0 | Implement SQLAlchemy |
| **CV** | Mocks | YOLO + DeepSORT | Complete | High | P0 | Implement PyTorch pipeline |
| **SUMO** | None | TraCI connection | Complete | High | P0 | Build `.net.xml` and Python bridge |
| **Safety** | Logic exists | Inline enforcement | Wiring | Low | P0 | Wire engine to SUMO outputs |
| **Auth** | Mocks | OIDC/RBAC | Complete | High | P0 | Implement Auth middleware |
| **Dashboard** | Streamlit Mock | Live React/Streamlit | Complete | Med | P0 | Build live real-time dashboard |
| **CI/CD** | None | Secure pipeline | Complete | Low | P1 | Implement Github Actions |

---

## 17. B1.16 & B1.17 — Implementation Priority

**P0 blockers:**
1. Setup FastAPI Application Shell and Repository Structure.
2. Setup PostgreSQL/PostGIS + SQLAlchemy persistence.
3. Build the actual PyTorch/OpenCV YOLO pipeline.
4. Integrate SUMO and TraCI for simulation.

**P1 improvements:** Prediction, Multi-tenancy, Digital Twin, CI/CD.
**P2 future capabilities:** AI Agents, Knowledge Graph, Quantum.

**Recommended implementation order:**
1. Database & API Foundation (Sprint 1)
2. Vision & Speed (Sprints 2 & 3)
3. Traffic Logic & SUMO (Sprints 4 & 5)
4. Safety & Optimization (Sprints 6 & 7)

**Files that should be modified first:**
- `app.py` / `main.py` (Need to become real FastAPI servers).
- `src/platform/data/database.py` (Needs to be created).
- `docker-compose.yml` (Needs Postgres/Redis configuration).
