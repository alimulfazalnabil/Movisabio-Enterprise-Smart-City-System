"""Send deterministic perception scenarios to a running MoviSabio gateway."""

from __future__ import annotations

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SCENARIOS = [
    {
        "intersection_id": "INT-001",
        "vehicle_id": "SIM-NORMAL-001",
        "lane_departure_detected": False,
        "curvature_radius": 80.0,
        "collision_risk_score": 0.12,
        "fused_objects_count": 4,
    },
    {
        "intersection_id": "INT-001",
        "vehicle_id": "SIM-DEPARTURE-001",
        "lane_departure_detected": True,
        "curvature_radius": 28.0,
        "collision_risk_score": 0.62,
        "fused_objects_count": 11,
    },
    {
        "intersection_id": "INT-001",
        "vehicle_id": "SIM-CRITICAL-001",
        "lane_departure_detected": True,
        "curvature_radius": 16.0,
        "collision_risk_score": 0.94,
        "fused_objects_count": 23,
    },
]


def post_scenario(endpoint: str, scenario: dict[str, object]) -> dict[str, object]:
    request = Request(
        endpoint,
        data=json.dumps(scenario).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the running gateway",
    )
    args = parser.parse_args()
    endpoint = f"{args.base_url.rstrip('/')}/api/v1/perception/telemetry/ingest"

    for scenario in SCENARIOS:
        try:
            response = post_scenario(endpoint, scenario)
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"{scenario['vehicle_id']}: request failed: {error}")
            return 1

        evaluation = response["safety_evaluation"]
        print(
            f"{scenario['vehicle_id']}: "
            f"critical={evaluation['critical_alert']} "
            f"action={evaluation['recommended_action']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())