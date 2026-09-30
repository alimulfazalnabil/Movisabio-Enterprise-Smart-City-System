
import random

from locust import HttpUser, task, between

class AITCSLoadTestUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_intersection_state(self):
        self.client.get("/api/v1/aitcs/intersections/INT-001/state")

    @task(3)
    def check_global_health(self):
        self.client.get("/api/v1/observability/health")

    @task(2)
    def ingest_perception_telemetry(self):
        self.client.post(
            "/api/v1/perception/telemetry/ingest",
            json={
                "intersection_id": "INT-001",
                "vehicle_id": f"SIM-{random.randint(1, 10000)}",
                "lane_departure_detected": random.random() < 0.05,
                "curvature_radius": round(random.uniform(20.0, 120.0), 2),
                "collision_risk_score": round(random.random(), 3),
                "fused_objects_count": random.randint(0, 20),
            },
            name="perception telemetry ingest",
        )
