from pathlib import Path

import pytest

from backend.app.simulation.adapters import SUMOAdapter


def test_missing_config_fails_before_starting_sumo(tmp_path: Path):
    adapter = SUMOAdapter(str(tmp_path / "missing.sumocfg"))

    with pytest.raises(FileNotFoundError):
        adapter.start_simulation()


def test_step_rejects_non_positive_interval():
    adapter = SUMOAdapter("scenario.sumocfg")

    with pytest.raises(ValueError):
        adapter.step(0)

    with pytest.raises(ValueError):
        adapter.step(-1)


def test_signal_command_rejects_invalid_values():
    adapter = SUMOAdapter("scenario.sumocfg")

    with pytest.raises(ValueError):
        adapter.set_signal_state("INT-001", -1, 10)

    with pytest.raises(ValueError):
        adapter.set_signal_state("INT-001", 0, 0)
