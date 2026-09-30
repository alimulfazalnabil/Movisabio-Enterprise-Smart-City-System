from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_ingest_lane_telemetry_returns_processed_perception():
    response = client.post(
        "/api/v1/perception/lane-telemetry",
        json={
            "intersection_id": "intersection-12",
            "lane_departure_detected": True,
            "curvature": 0.18,
            "obstacle_risk_level": "HIGH",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "processed_perception": {
            "intersection_id": "intersection-12",
            "lane_departure_detected": True,
            "curvature": 0.18,
            "obstacle_risk_level": "HIGH",
        },
    }


def test_ingest_lane_telemetry_requires_all_fields():
    response = client.post(
        "/api/v1/perception/lane-telemetry",
        json={"intersection_id": "intersection-12"},
    )

    assert response.status_code == 422


def test_ingest_perception_telemetry_returns_safety_evaluation():
    response = client.post(
        "/api/v1/perception/telemetry/ingest",
        json={
            "intersection_id": "intersection-12",
            "vehicle_id": "vehicle-7",
            "lane_departure_detected": False,
            "curvature_radius": 42.5,
            "collision_risk_score": 0.9,
            "fused_objects_count": 6,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["perception_record"]["vehicle_id"] == "vehicle-7"
    assert body["safety_evaluation"]["critical_alert"] is True
    assert body["safety_evaluation"]["recommended_action"] == (
        "EMERGENCY_BRAKING_RECOMMENDED"
    )


def test_perception_history_is_filtered_by_intersection():
    response = client.get("/api/v1/perception/history/intersection-12")

    assert response.status_code == 200
    body = response.json()
    assert body["intersection_id"] == "intersection-12"
    assert body["total_records"] >= 1
    assert all(
        record["intersection_id"] == "intersection-12"
        for record in body["records"]
    )