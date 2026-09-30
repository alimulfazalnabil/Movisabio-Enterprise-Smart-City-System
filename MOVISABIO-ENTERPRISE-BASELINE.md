# MoviSabio Enterprise Baseline

## 1. Current Architecture & Repository State

An initial audit of the repository reveals a monolithic structure that has evolved organically through rapid prototyping and feature additions.

### Discovered Directories
- `aitcs/`: Contains `application/`, `domain/`, `infrastructure/`, `presentation/`. This seems to be the legacy core containing many engine modules (e.g., `rl_engine.py`, `safety_engine.py`).
- `backend/services/`: Contains various disconnected domain scripts (e.g., `drone_dispatch.py`, `waste_management.py`).
- `platform/`: The newly created enterprise foundational layer containing `database/`, `config/`, `identity/`, `api_gateway/`, `device_registry/`, `event_bus/`.
- `apps/` and `src/`: Contain various application entry points (`app.py`, `main_enterprise.py`, `main.py`).
- `frontend/`: Standalone Vite/React frontend app.
- `deploy/`, `deployment/`, `helm/`, `infra/`, `infrastructure/`, `terraform/`: Fragmented infrastructure configurations.
- `tests/`: Fragmented unit and integration tests.

### Identified Gaps
1. **Directory Fragmentation:** We have overlapping domain directories (`aitcs`, `backend`, `platform`, `src`, `services`). Code resides across multiple disjointed locations.
2. **Infrastructure Duplication:** `deploy/`, `deployment/`, `helm/`, `infra/`, `infrastructure/`, and `terraform/` all exist.
3. **No Central API Gateway:** Legacy APIs are scattered in `aitcs/presentation/` and `backend/services/`, while the new enterprise gateway sits in `platform/api_gateway/`.
4. **Data Layer Gap:** Although Phase A introduced `platform/database/`, the legacy modules in `aitcs/` still rely on hardcoded state or lack tenant-awareness.
5. **No Clear Control vs. Data Plane Separation:** Domain logic, platform tools, and AI algorithms are co-located in ways that blur boundaries.

---

## 2. Target Architecture

We will restructure the repository to adhere strictly to the target 5-layer enterprise architecture:

### 2.1 MoviSabio 5-Layer Platform Architecture

1. **EXPERIENCE (apps/)**: `web`, `edge`, `dashboard`
2. **PLATFORM (platform/)**: `auth`, `tenancy`, `billing`, `audit`, `database`, `api_gateway`
3. **INTELLIGENCE (services/intelligence/)**: `cv`, `prediction`, `rl`, `digital_twin`, `territorial`
4. **CONTROL (services/control/)**: `safety_engine`, `traffic_controller`, `device_management`, `iot`
5. **REAL WORLD (infrastructure/edge/)**: `cctv`, `sensors`, `signals`

### 2.2 Standardized Repository Tree

```
MoviSabio/
├── apps/               # Entrypoints and UI (api, web, edge)
├── platform/           # Cross-cutting foundational modules (auth, tenancy, db)
├── services/           # Domain-specific business logic (traffic, prediction, iot)
├── packages/           # Shared libraries (schemas, domain entities, utils)
├── infrastructure/     # Consolidated IaC (terraform, docker, k8s, monitoring)
├── tests/              # Unified test suite (unit, integration, e2e)
├── docs/               # Enterprise documentation
└── scripts/            # Build & migration tooling
```

---

## 3. Implementation Sequence (Phase A & B)

### Step 1: File and Directory Consolidation
- Consolidate all infrastructure code into `infrastructure/` (retire `deploy`, `deployment`, `helm`, `infra`, `terraform`).
- Move all domain modules from `aitcs/` and `backend/` into `services/`.
- Move entry point files into `apps/api/` and `apps/web/`.
- Retire redundant or legacy root-level folders safely.

### Step 2: Database & Tenancy Hardening
- Complete `alembic` setup for `platform/database/migrations`.
- Ensure all business queries apply tenant scoping automatically via DB session.

### Step 3: API & Error Normalization
- Enforce standard `/api/v1` structure across all modules in `services/`.
- Implement standard enterprise error schemas (RFC 7807/Custom).

### Step 4: Observability & Health
- Add standard OpenTelemetry logging and `/health/live`, `/health/ready` endpoints globally.

### Step 5: CI/CD Quality Gate
- Unify `.github/workflows/` to enforce linting, formatting, security scanning, and test coverage before merges.

---

*This document serves as the formal baseline. The immediate next action is executing Step 1 of the Implementation Sequence to consolidate the repository.*
