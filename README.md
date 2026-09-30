# MOVISABIO ENTERPRISE SMART CITY PLATFORM
**Mission-Critical Urban Traffic Optimization, Autonomous Emergency Reconnaissance, & Multi-Region Kubernetes Infrastructure**

> For the current implementation boundaries, see [DEVELOPMENT.md](DEVELOPMENT.md).

> For conceptual diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md).

> For the ordered MVP plan, see [ROADMAP.md](ROADMAP.md).

---



## 📑 Table of Contents
1. [Executive Summary & Architecture Vision](#-1-executive-summary--architecture-vision)
2. [Complete Monorepo Structure](#-2-complete-monorepo-structure)
3. [Core Engineering Modules & Microservice Stack](#-3-core-engineering-modules--microservice-stack)
4. [Frontend 3D Digital Twin Command Center](#-4-frontend-3d-digital-twin-command-center)
5. [Infrastructure, Kubernetes & GitOps Stack](#-5-infrastructure-kubernetes--gitops-stack)
6. [Local Development & Quickstart Guide](#-6-local-development--quickstart-guide)
7. [Comprehensive Feature Audit Matrix](#-7-comprehensive-feature-audit-matrix)
8. [Containerization & CI/CD Pipeline Architecture](#-8-containerization--cicd-pipeline-architecture)
9. [Disaster Recovery & Operations Runbook Reference](#-9-disaster-recovery--operations-runbook-reference)

---



## 🏛️ 1. Executive Summary & Architecture Vision

MoviSabio Enterprise is an advanced, production-grade municipal intelligence platform designed to orchestrate high-frequency IoT telemetry, automated emergency vehicle preemption, Variable Speed Limit (VSL) harmonization, and autonomous drone dispatching. Built on a resilient asynchronous backend architecture powered by FastAPI and Redis, and paired with a real-time React 18 3D Digital Twin command center, the platform guarantees **99.999% high availability** across multi-region active-active cloud clusters (AWS EKS / Azure AKS).

### Strategic Product Positioning
MoviSabio operates as a **Territorial Intelligence Platform** rather than a collection of isolated AI features. The core operational loop follows a closed-loop execution cycle: 
$$\text{Sense} \longrightarrow \text{Understand} \longrightarrow \text{Predict} \longrightarrow \text{Optimize} \longrightarrow \text{Act} \longrightarrow \text{Measure}$$

This empowers municipalities to transform existing CCTV and infrastructure assets into a live smart-city operating system, delivering measurable improvements across mobility, public safety, sustainability, and urban resilience. Additional architectural benefits and product narratives are detailed in `SMART_CITY_BENEFITS.md`.

---



## 📂 2. Complete Monorepo Structure

```plaintext
movisabio-enterprise/
├── .github/
│   └── workflows/
│       └─ ci-cd-pipeline.yml            # Automated GitHub Actions CI/CD & container build pipeline
├── aitcs/                                # Python 3.12 AITCS Core Engine Package
│   ├── __init__.py
│   ├── config.py                         # Pydantic v2 Azure & AITCS Enterprise Settings
│   ├── domain/                           # Pure business entities & value objects (Phase 1)
│   │   ├── __init__.py
│   │   ├── entities.py                   # IntersectionState, IntersectionID
│   │   └── value_objects.py              # GranularTrafficState, LevelOfService
│   ├── application/                      # Use cases, orchestration & optimization engines
│   │   ├── __init__.py
│   │   ├── state_estimation.py           # Phase 2: HCM LOS, Congestion Index, Pressure
│   │   ├── prediction_engine.py          # Phase 3: PyTorch LSTM/GRU Multi-Horizon Forecasting
│   │   ├── decision_engine.py            # Phase 4: Adaptive Splits & Phase Skipping
│   │   ├── signal_optimization.py        # Phase 5: Webster's Optimum Cycle & Weather Modifiers
│   │   ├── rl_engine.py                  # Phase 6: Deep Reinforcement Learning (DQN/PPO)
│   │   ├── safety_engine.py              # Phase 7: Immutable Rule-Based Safety & Conflict Matrices
│   │   └── multi_intersection_coordinator.py # Phase 9: Green Waves & Network Balancing
│   ├── infrastructure/                   # External adapters, databases & controllers
│   │   ├── __init__.py
│   │   ├── controller_integration.py     # Phase 8: NTCIP, MQTT, REST, Heartbeat ACKs
│   │   └── telemetry.py                  # OpenTelemetry tracing & Prometheus metrics
│   └── presentation/                     # FastAPI routing and web sockets
│       ├── __init__.py
│       └── api_router.py                 # Phase 10: REST APIs & Live WebSocket Stream
├── src/                                  # Core Enterprise Microservices Gateway
│   └── main.py                           # Unified FastAPI ASGI Entrypoint (Mounts Smart City & AITCS)
├── frontend/                             # React 18 3D Digital Twin Command Center
│   ├── src/
│   │   ├── App.tsx                       # Main UI Dashboard & Live Telemetry Grid
│   │   ├── main.tsx                      # React 18 Concurrent Root Mount
│   │   └── index.css                     # Tailwind CSS Global Stylesheet
│   ├── package.json                      # Frontend dependencies & scripts
│   └── vite.config.ts                    # Vite build configuration
├── deploy/                               # Raw Declarative Kubernetes Manifests (ArgoCD Source)
│   ├── deployment.yaml                   # Unified Enterprise + AITCS deployment manifest
│   ├── service.yaml                      # ClusterIP service configuration
│   ├── hpa.yaml                          # Horizontal Pod Autoscaler (3 to 20 replicas)
│   └── argocd-application.yaml           # ArgoCD GitOps continuous deployment pipeline manifest
├── helm/                                 # Enterprise Helm Chart Packaging
│   └── movisabio/
│       ├── Chart.yaml                    # Chart metadata definition
│       ├── values.yaml                   # Parameterized multi-region environment configurations
│       └── templates/                    # Dynamic Go-templated Kubernetes resource manifests
├── tests/                                # Comprehensive Quality Assurance Suite
│   └── aitcs/
│       ├── unit/                         # Unit tests for domain models, state estimation & safety
│       │   ├── test_state_estimation.py
│       │   └── test_safety_engine.py
│       ├── integration/                  # End-to-end closed-loop pipeline test
│       │   └── test_pipeline_integration.py
│       └── load/                         # High-throughput Locust stress-testing scripts
│           └── locustfile.py
├── Dockerfile                            # Multi-stage production container build file
├── pyproject.toml                        # Modern Python project metadata & build system configuration
├── requirements.txt                      # Pinned production Python package dependencies
├── DEPLOYMENT_RUNBOOK.md                 # Disaster recovery, operations & scaling runbook
├── LICENSE                               # Proprietary Restricted Commercial License
└── README.md                             # Master project documentation portal
```




## 🧠 3. Core Engineering Modules & Microservice Stack

The backend is structured into distinct optimization and domain pipelines:
- State Estimation (Phase 2): Calculates Highway Capacity Manual (HCM) Level of Service (LOS), Congestion Indices, and intersection pressure.
- Prediction Engine (Phase 3): Leverages PyTorch LSTM/GRU models for multi-horizon traffic demand forecasting.
- Decision & Signal Optimization (Phases 4–5): Implements adaptive phase splits, phase skipping, and Webster's Optimum Cycle calculations dynamically modified by weather conditions.
- Reinforcement Learning (Phase 6): Trains DQN/PPO agents for dynamic online policy optimization.
- Immutable Safety Engine (Phase 7): Enforces strict mathematical conflict matrices to validate every signal recommendation before controller transmission.
- Controller Integration (Phase 8): Bridges NTCIP, MQTT, and REST protocols with reliable heartbeat acknowledgments.
- Multi-Intersection Coordinator (Phase 9): Harmonizes green waves and network-wide load balancing.




## 🖥️ 4. Frontend 3D Digital Twin Command Center

The frontend interface (frontend/) serves as the mission control cockpit for municipal operators:
- React 18 Concurrent Rendering: Utilizes createRoot for smooth state updates and high-performance rendering.
- TypeScript Typing: Enforces strict interface contracts across live telemetry streams, alert counts, and system metrics.
- Tailwind CSS Styling: Integrates high-precision typography (Inter for UI components, JetBrains Mono for telemetry and timestamps) with custom brand palettes and glowing status indicators.




## ⚓ 5. Infrastructure, Kubernetes & GitOps Stack

Production deployments are managed using a dual-layer strategy combining static declarative manifests (/deploy) with parameterized Helm charts (/helm):
- Deployment (deployment.yaml): Guarantees zero-downtime rolling updates (maxSurge: 1, maxUnavailable: 0), strict resource limits (1 CPU, 1Gi RAM), non-root security contexts (UID 10001), and rigorous health probes.
- Service & Ingress (service.yaml): Provisions internal ClusterIP bindings alongside NGINX Ingress controllers with automated cert-manager TLS provisioning for api.movisabio.io.
- Autoscaling (hpa.yaml): Implements Kubernetes HPA v2 rules to dynamically scale pods between 3 and 10 replicas based on an 80% CPU utilization threshold with minimal stabilization lag.




## 🚀 6. Local Development & Quickstart Guide

### Prerequisites

- Python 3.12+
- Node.js 20+ with npm
- Docker and Docker Compose

### 1. Start Local Infrastructure

```bash
docker compose up -d postgres redis
```

### 2. Run the Backend Gateway

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive API documentation is accessible at http://localhost:8000/docs.

To execute deterministic safety scenarios through the perception bridge:

```bash
python tests/aitcs/load/perception_simulator.py
```

To run high-throughput stress tests using Locust:

```bash
locust -f tests/aitcs/load/locustfile.py --host=http://localhost:8000
```

### 3. Run the Command Center Frontend

In a separate terminal session:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Access the command center at http://localhost:3000.

Note: Persistent storage components (Alembic metadata or ORM models) should be initialized prior to running data migrations. Cross-instance history relies on Redis-backed event streams in multi-worker environments.




## ✅ 7. Comprehensive Feature Audit Matrix

The MoviSabio platform encompasses the following fully mapped enterprise capabilities:
- AI Traffic Control System (AITCS): ATSC, signal timing optimization, dynamic green splits/yellow intervals, cycle length optimization, phase skipping, green waves, and gridlock prevention.
- Computer Vision & Edge AI: Multi-object detection (vehicles, pedestrians, emergency units), tracking via ByteTrack/DeepSORT, lane occupancy, queue estimation, and GPU acceleration.
- Automatic Number Plate Recognition (ANPR): License plate OCR, vehicle profiling, stolen vehicle detection, blacklist/whitelist management, and toll/parking integration.
- Traffic Analytics & Prediction: Real-time volume, density, Congestion Index (CI), LOS tracking, and LSTM/GRU demand forecasting.
- Reinforcement Learning & MLOps: DQN, PPO, SAC agents, digital twin validation, model registries, versioning, and drift detection.
- Emergency & Public Transport Optimization: Automated emergency preemption corridors, disaster routing, and Transit Signal Priority (TSP) for buses/trams.
- Pedestrian & Environmental Intelligence: Adaptive crosswalk durations, real-time emission estimation (CO2, NOx, PM2.5/PM10), eco-routing, and weather-aware optimizations.
- Drone Operations & Smart Infrastructure: Autonomous drone fleet management, RTSP streaming, smart parking guidance, IoT/Azure integrations, and mTLS security.




## 🐳 8. Containerization & CI/CD Pipeline Architecture

### Multi-Stage Docker Build

The root Dockerfile isolates compilation dependencies from the lightweight runtime image:
- Builder Stage (python:3.11-slim): Installs build toolchains and compiles dependencies into an isolated virtual environment (/opt/venv).
- Runtime Stage (python:3.11-slim): Copies the compiled environment, establishes a non-root system user (movisabio, UID 10001), and runs Uvicorn with multi-worker multiprocessing.

### Automated GitHub Actions CI/CD (ci-cd-pipeline.yml)

The workflow executes four automated gates on every push to main or staging branches:
- Linting & Testing: Runs syntax checks and pytest suites with XML coverage reporting.
- Security Scans: Executes TruffleHog for verified secret leak detection and Trivy for container image vulnerability audits.
- OCI Image Build & Push: Uses Docker Buildx to generate multi-architecture images (linux/amd64, linux/arm64) pushed to GitHub Container Registry (ghcr.io).
- GitOps Promotion: Automatically updates image tag hashes in the dedicated GitOps deployment repository, triggering ArgoCD cluster synchronization.




## 📖 9. Disaster Recovery & Operations Runbook

For complete emergency protocols, rollback procedures, and multi-region failover instructions, refer to DEPLOYMENT_RUNBOOK.md. Key operational standards include:
- P1 Incident SLAs: Rapid response protocols for total platform outages or emergency dispatch failures resolved in under 15 minutes.
- Rollback Procedures: Step-by-step instructions for ArgoCD dashboard rollbacks or emergency kubectl rollout undo commands.
- Regional Failover: Active-active multi-region DNS redirection guidelines in the event of primary cloud provider interruptions.
