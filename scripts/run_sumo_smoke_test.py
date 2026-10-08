"""Run a deterministic SUMO/TraCI smoke test for AICTS-05.1.

Usage:
    python scripts/run_sumo_smoke_test.py --config path/to/scenario.sumocfg --steps 100 --seed 42
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from backend.app.simulation.adapters import SUMOAdapter


def main() -> int:
    parser = argparse.ArgumentParser(description="AICTS-05.1 SUMO smoke test")
    parser.add_argument("--config", required=True, help="Path to a SUMO .sumocfg file")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--step-length", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.steps <= 0:
        parser.error("--steps must be greater than zero")
    if args.step_length <= 0:
        parser.error("--step-length must be greater than zero")

    adapter = SUMOAdapter(args.config, seed=args.seed)

    try:
        adapter.start_simulation()

        first = adapter.step(args.step_length)
        last = first

        for _ in range(args.steps - 1):
            last = adapter.step(args.step_length)

        print(json.dumps({
            "status": "PASS",
            "config": str(Path(args.config).resolve()),
            "seed": args.seed,
            "steps": args.steps,
            "simulation_time_s": last.simulation_time_s,
            "vehicle_count": last.vehicle_count,
            "remaining_vehicles": last.remaining_vehicles,
        }, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }, indent=2))
        return 1
    finally:
        adapter.close()


if __name__ == "__main__":
    sys.exit(main())
