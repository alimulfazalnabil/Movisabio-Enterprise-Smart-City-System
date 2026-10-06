# Phase B1 — Full Repository Audit & Architecture Gap Matrix

## 1. Executive Summary

This document establishes the exact delta between the frozen MoviSabio Enterprise Platform Architecture (A4.37) and the current state of the GitHub repository. It acts as the definitive ledger of technical debt, existing capabilities, and the required implementation roadmap for Phase B.

The current repository contains a highly developed **logical domain model** (Python Pydantic schemas, isolated domain stubs, and unit tests). It successfully demonstrates the architectural relationships across 50+ domains. However, it lacks the **production scaffolding** necessary to run as a live, cyber-physical platform (e.g., FastAPIs, databases, Docker, CV models, Kafka, UI).

## 2. Component Target vs Current Matrix

| Component | Architecture Target | Current Repository State | Status | Priority |
|---|---|---|---|---|
| **Backend API** | FastAPI production API | Headless logic only. No endpoints or routers. | 🔴 Missing | P0 |
| **PostgreSQL/PostGIS** | Multi-tenant spatial DB | In-memory Python dictionaries. No ORM or DB connections. | 🔴 Missing | P0 |
| **Authentication** | OIDC/OAuth2 | Stubbed `SecurityManager`. No real auth mechanism. | 🔴 Missing | P0 |
| **RBAC** | RBAC + ABAC | Domain models defined. Logic is mocked. | 🟡 Partial | P0 |
| **Traffic ingestion** | Production ingestion | Domain schemas exist (`TrafficDetection`). No actual stream ingestion. | 🔴 Missing | P0 |
| **YOLO detection** | Vehicle detection | Blank/stub CV directories. No PyTorch/ONNX models integrated. | 🔴 Missing | P0 |
| **Tracking** | Multi-object tracking | Schemas exist. No DeepSORT/ByteTrack implementation. | 🔴 Missing | P0 |
| **Lane counting** | Lane-wise analytics | Stubs exist in `src/domain/traffic`. | 🔴 Missing | P0 |
| **Speed estimation** | Calibrated estimation | Logic modeled, but no real-world homography/perspective logic. | 🔴 Missing | P0 |
| **Traffic state** | Congestion intelligence | Robust schemas and mock calculators exist. | 🟡 Partial | P0 |
| **Prediction** | Forecasting | ML architecture stubbed. No actual TensorFlow/PyTorch prediction code. | 🔴 Missing | P1 |
| **SUMO** | Simulation | Traci/SUMO schemas exist. No actual SUMO `.net.xml` or TraCI loops. | 🔴 Missing | P0 |
| **RL optimization** | DQN/PPO/etc. | Defined in architecture. Not present in code. | 🔴 Missing | P1 |
| **Safety engine** | Hard constraints | High-quality logic implemented and tested (`SafetyEngine`). Needs DB persistence. | 🟢 Ready | P0 |
| **Signal controller** | Individual signal control | Mock classes only. | 🔴 Missing | P0 |
| **Dashboard** | Operational dashboard | No frontend code (React or Streamlit) exists. | 🔴 Missing | P0 |
| **Audit** | Decision/action audit | `ActionLedger` built and tested. Needs DB backend. | 🟢 Ready | P0 |
| **Observability** | Metrics/logging/tracing | Only standard `print` or `logging`. No OpenTelemetry. | 🔴 Missing | P0 |
| **Docker** | Reproducible deployment | No `Dockerfile` or `docker-compose.yml`. | 🔴 Missing | P0 |
| **CI/CD** | Automated pipeline | No GitHub Actions workflows. | 🔴 Missing | P1 |
| **Digital Twin** | Territorial sim state | Domain logic exists. Not wired to a real state machine. | 🟡 Partial | P1 |
| **Knowledge Graph** | Semantic intelligence | Modeled in architecture. | 🔴 Missing | P2 |
| **AI Agents** | Governed autonomy | `OversightEngine` built. Agent runtimes missing. | 🟡 Partial | P2 |
| **Multi-tenancy** | Enterprise SaaS | Tenancy models defined. Not enforced in an API layer. | 🟡 Partial | P1 |
| **Edge runtime** | Offline/edge operation | Defined in architecture. | 🔴 Missing | P1 |

## 3. Structural & Code Audit

### Existing Components (The Good)
- **Domain Logic:** `src/domain/` contains 50+ beautifully modeled domains.
- **Platform Intelligence:** `src/platform/` contains excellent logic for Anomaly Detection, Safety Constraints, Action Ledgers, and Policy Engines.
- **Testing:** `tests/` contains comprehensive unit tests that validate the logic.

### Incomplete/Missing Components (The Gaps)
- **Application Shell:** There is no `app.py`, `main.py`, or `FastAPI` instance to serve this logic over the network.
- **State Persistence:** Everything is stateless or relies on in-memory dictionaries. `SQLAlchemy` (and `GeoAlchemy2` for spatial) must be introduced.
- **Physical World Bridge:** The system cannot process an actual `.mp4` video file or an RTSP stream. OpenCV/YOLO are entirely missing.
- **Environment Management:** No `requirements.txt` (though `pyproject.toml` might exist, missing major ML/DB packages), `.env` handling, or Docker environments.

### Architectural Violations
- **Data Isolation:** Mock DBs in `src/domain/` often bleed context. A proper Dependency Injection (DI) pattern is needed once FastAPI is introduced.
- **Tight Coupling:** Without a message bus (like Kafka), domain models might start calling each other directly, breaking event-driven isolation.

## 4. Recommended Implementation Order (Sprint Plan)

We will follow the exact priority structure requested. Antigravity will be prompted to implement these one by one, keeping credit usage efficient and targeted.

### **Sprint 1 — Foundation (P0)**
*Objective: Build the application shell.*
- Initialize Docker Compose (PostgreSQL, PostGIS, Redis).
- Setup FastAPI structure (`src/apps/api`).
- Configure SQLAlchemy and Alembic for database migrations.
- Establish baseline logging and health check endpoints.

### **Sprint 2 — Vision (P0)**
*Objective: Open the system's eyes.*
- Implement `yolov8` (or similar) vehicle detection pipeline in Python.
- Add DeepSORT/ByteTrack for multi-object tracking.
- Create virtual lane polygon configurations for camera feeds.

### **Sprint 3 — Speed (P0)**
*Objective: Measure physics.*
- Implement homography matrix calculations.
- Calculate speed based on pixel-to-meter conversion across tracked trajectories.

### **Sprint 4 — Traffic Intelligence (P0)**
*Objective: Understand the roads.*
- Convert raw vehicle counts and speeds into `TrafficState` (congestion levels).
- Persist these states to the PostGIS database.

### **Sprint 5 — SUMO (P0)**
*Objective: Simulate the physical world.*
- Integrate Eclipse SUMO and `traci` Python library.
- Synchronize real-world `TrafficState` to SUMO network inputs.

### **Sprint 6 — Optimization & Safety (P0)**
*Objective: Decide and Govern.*
- Connect a basic Optimization Baseline to the SUMO simulation.
- Wire the output through the existing `SafetyEngine` to ensure it never violates hard constraints (e.g., minimum green times).

### **Sprint 7 — Dashboard (P0)**
*Objective: Human visibility.*
- Build a rapid Streamlit (or React) dashboard showing the live camera feed, bounding boxes, live traffic state, and signal recommendations.

## 5. Next Action
The highest-value next step is to begin **Sprint 1 — Foundation**. I will await the explicit command to initialize the FastAPI shell, SQLAlchemy, and Docker configurations.
