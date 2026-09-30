# Development guide

This guide describes the repository as it currently works. It helps new contributors locate executable code without assuming that every component described in the `README` is already integrated.

Conceptual diagrams are maintained in [ARCHITECTURE.md](ARCHITECTURE.md). Delivery order and MVP scope are maintained in [ROADMAP.md](ROADMAP.md).

## What runs today

The main process is `src.main:app`, a FastAPI application that exposes:

- combined telemetry analysis under `/api/v1/aitcs`;
- basic lane telemetry at `/api/v1/perception/lane-telemetry`;
- perception ingestion and history under `/api/v1/perception`;
- gateway status and health endpoints.

Routers for drones, transit, parking, V2X, pedestrians, and municipal services exist under `aitcs/presentation`, but they are not included in the main gateway yet.

Lane detection and the perception bridge are already part of AITCS and are mounted by the main gateway. Their current endpoints are integrated, although their payloads and in-memory state still need production hardening.

`backend/services` contains independent FastAPI applications. Each file exposes its own `app` object and is not part of `src.main:app`. The current `docker-compose.yml` starts only the main gateway and observability service, in addition to Redis and PostgreSQL.

## Code map

- `aitcs/domain`: pure traffic-domain data structures.
- `aitcs/application`: calculations and business rules that can generally be instantiated and tested without FastAPI.
- `aitcs/infrastructure`: adapters for controllers, metrics, and spatial data.
- `aitcs/presentation`: HTTP models and FastAPI routers.
- `src/main.py`: composition root for the application served by the main container.
- `backend/services`: standalone municipal services based on FastAPI and Redis.
- `frontend`: React/Vite dashboard.
- `tests/aitcs`: unit, integration, and load tests for the AITCS core.

## Main flow

The pipeline covered by `tests/aitcs/integration/test_pipeline_integration.py` is:

1. `TrafficStateEstimationService` normalizes telemetry and estimates congestion.
2. `TrafficPredictionEngine` produces forecasts for fixed time horizons.
3. `AIDecisionEngine` proposes a signal phase and timing.
4. `SafetyValidationEngine` limits or replaces the proposal before it reaches a controller.

Safety validation should remain a mandatory boundary if this pipeline is connected to physical infrastructure.

## State and persistence

Several engines keep state in process-local lists or dictionaries. This state:

- is lost on restart;
- is not shared between Uvicorn workers;
- is not backed by PostgreSQL or Redis.

This affects perception history, incidents, citizen reports, the drone fleet, V2X messages, and the controller registry, among other components.

Although PostgreSQL/PostGIS settings exist, the current spatial repository uses fixed in-memory data. PyTorch model weights are not loaded from a registry or checkpoint, so their results do not represent a trained model yet. Digital-twin steps, utility-grid readings, and parts of the drone/controller operations are also simulated.

## Local development

Backend:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pip install pytest
pytest
uvicorn src.main:app --reload --port 8000
```

OpenAPI documentation is available at `http://localhost:8000/docs`.

Frontend:

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

The frontend reads `VITE_API_BASE_URL` and falls back to `http://localhost:8000` when it is not defined.

## Before extending a feature

- Confirm whether it belongs in the gateway or a standalone service.
- Avoid global state when more than one worker may be used.
- Keep pure calculations separate from Redis, database, and network access.
- Add engine-level tests before exposing a new endpoint.
- Document the units and valid ranges of numeric values.
- Never send a signal decision without passing it through `SafetyValidationEngine`.

## Visible technical debt

- Declared versions differ between the package, API, frontend, and CI image.
- CI uses Python 3.11 while the package and container declare Python 3.12.
- The `README` describes production, high-availability, and 3D capabilities that are still partial or simulated.
- Some routers contain unused WebSocket and HTTP exception imports.
- The security service imports `python-jose`, but the dependency is not declared.
- Most applications under `backend/services` have no automated tests or deployment composition.
- The frontend combines real perception records with simulated metrics and statuses.

These limitations do not prevent experimentation with the core, but they should be addressed before presenting the repository as an operational production platform.
