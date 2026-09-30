# MVP roadmap

This roadmap defines the shortest path to a production MVP based on the perception and lane-detection capabilities already integrated into AITCS (AI Traffic Control System). The component model and system boundaries are documented in [ARCHITECTURE.md](ARCHITECTURE.md).

## MVP goal

Operate one pilot intersection with live camera-derived observations from the integrated AITCS perception subsystem, fully audited decisions, and supervised delivery to a real roadside controller:

1. ingest a versioned camera observation;
2. estimate the current traffic state;
3. produce a deterministic signal proposal;
4. enforce safety rules;
5. require operator approval during the MVP pilot;
6. deliver the approved command and record its acknowledgement;
7. display the complete observation-to-command trace to an operator.

## 0. Consolidate the existing perception path and pilot scope

- Inventory `LaneTelemetryPayload`, `PerceptionPayload`, and the combined AITCS telemetry payload as parts of the already integrated perception path.
- Define a canonical `CameraObservation v1` contract that preserves the useful existing fields and adds identity, UTC timestamps, ordering, traffic values, confidence, health, model version, and calibration version.
- Keep existing routes as adapters where compatibility is useful instead of building a second perception service.
- Record any decision inputs that the current AITCS perception subsystem does not produce and assign their ownership explicitly.
- Agree on transport, authentication, publish frequency, latency and freshness limits, retry behavior, and sample fixtures.
- Select one pilot intersection, its controller protocol, the safe fallback plan, and the operational owner.
- Identify the responsible traffic engineer, road authority, controller vendor, OT security owner, and privacy owner required to approve field operation.
- Define replay, shadow, supervised, and autonomous mode semantics.
- Keep LSTM, reinforcement learning, drones, ANPR workflows, V2X, 3D rendering, and multi-region deployment out of scope.

**Exit:** the integrated perception routes and the traffic-control pipeline pass the same versioned contract fixtures, every required decision input has an owner, and the pilot has written acceptance and rollback criteria.

## 1. Harden the integrated camera-observation path

- Add an authenticated ingestion adapter for the agreed contract.
- Validate schema, event time, ordering, idempotency, confidence, and camera health.
- Buffer accepted observations and quarantine invalid or stale events.
- Add record-and-replay tooling using real, privacy-safe observation samples.
- Keep raw video and image retention inside the AITCS perception boundary by default.

**Exit:** the production ingestion path completes an agreed soak period with measured latency, loss, duplicate, stale-event, and rejection rates.

## 2. Build the durable decision pipeline

- Add one application orchestrator for observation, state estimate, decision, safety result, persistence, and delivery intent.
- Introduce repository interfaces at the application boundary.
- Use Redis for ingestion buffering, current state, and command delivery status.
- Use PostgreSQL for configuration and the immutable observation-to-decision audit trail.
- Remove request-critical state from module-level lists and dictionaries.
- Apply explicit fallback behavior when observations are missing, stale, unordered, unhealthy, or below the confidence threshold.

**Exit:** every accepted observation produces a deterministic, safety-validated, traceable decision, and gateway restarts do not lose configuration or audit history.

## 3. Run in production shadow mode

- Deploy the ingestion and decision pipeline against the live camera feed without sending controller commands.
- Compare recommendations with the active signal plan and investigate disagreements.
- Replace dashboard placeholders with API-backed camera health, state, decisions, and safety results.
- Add dependency-aware readiness checks, pipeline metrics, alerts, and an operator runbook.

**Exit:** the agreed shadow period completes within data-quality, latency, availability, and safety thresholds, with no unexplained decision path.

## 4. Start supervised actuation

- Implement the pilot controller protocol behind the controller port.
- Add a transactional command outbox, idempotent delivery, ACK, NACK, timeout, and bounded retry handling.
- Require an authorized operator to approve commands.
- Provide a kill switch and automatic rollback to the approved fallback signal plan.
- Run the first commands in controlled maintenance windows with field staff available.
- Treat traffic-engineering, authority, vendor, OT security, and privacy approval as release gates rather than software tasks.

**Exit:** the pilot sends supervised commands with complete audit and acknowledgement records, and every tested failure returns safely to the fallback plan.

## 5. Harden the production MVP

- Complete RBAC, restrictive CORS, secret validation, camera-producer authentication, and operator authorization.
- Align versions and the supported Python runtime.
- Add database migrations, backup and restore checks, dependency health, structured logs, traces, SLOs, and alert ownership.
- Make the production deployment reproducible and keep Docker Compose as the local integration environment.
- Add CI gates for contract, unit, API, persistence, replay, safety, and controller-adapter tests.
- Complete deployment, rollback, incident, camera-loss, and controller-loss runbooks.

**Exit:** the production-readiness checklist and recovery drill pass, and the supervised pilot can operate without developer intervention.

## Completion criteria

The MVP is complete when:

- real observations arrive through the versioned AITCS perception contract;
- data quality, camera health, freshness, ordering, and duplicate events are enforced;
- each observation produces a deterministic and fully traceable decision;
- state, configuration, and audit records survive a gateway restart;
- shadow mode has completed against the live production feed;
- supervised commands reach the pilot controller with idempotent delivery;
- ACK, NACK, and timeout paths are tested;
- camera loss, controller loss, operator pause, and the kill switch activate the approved fallback;
- the dashboard contains only API-backed production data or clearly labelled replay data;
- contract, API, persistence, safety, replay, and field-adapter tests pass in CI;
- deployment, rollback, audit, monitoring, and operational ownership are documented.

## Deferred until after the MVP

- trained forecasting and reinforcement-learning policies;
- advanced changes to the internal AITCS inference pipeline;
- fully autonomous actuation and network-wide rollout;
- drones, V2X, utilities, parking, and citizen-service integrations;
- 3D digital-twin rendering;
- Kubernetes, multi-region failover, and high-availability claims.
