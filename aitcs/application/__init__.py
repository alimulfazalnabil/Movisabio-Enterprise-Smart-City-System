"""AITCS application services with lazy public exports.

Keeping imports lazy prevents optional ML dependencies from blocking lightweight
engines, routers, and tests that do not use prediction or reinforcement learning.
"""

from importlib import import_module


_EXPORTS = {
    "TrafficStateEstimationService": ("state_estimation", "TrafficStateEstimationService"),
    "TrafficPredictionEngine": ("prediction_engine", "TrafficPredictionEngine"),
    "PredictionResult": ("prediction_engine", "PredictionResult"),
    "AIDecisionEngine": ("decision_engine", "AIDecisionEngine"),
    "SignalDecision": ("decision_engine", "SignalDecision"),
    "SignalOptimizationEngine": ("signal_optimization", "SignalOptimizationEngine"),
    "OptimizedSignalPlan": ("signal_optimization", "OptimizedSignalPlan"),
    "SafetyValidationEngine": ("safety_engine", "SafetyValidationEngine"),
    "SanitizedSignalCommand": ("safety_engine", "SanitizedSignalCommand"),
    "MultiIntersectionCoordinator": (
        "multi_intersection_coordinator",
        "MultiIntersectionCoordinator",
    ),
    "GreenWaveCorridor": ("multi_intersection_coordinator", "GreenWaveCorridor"),
}


def __getattr__(name: str):
    try:
        module_name, attribute_name = _EXPORTS[name]
    except KeyError as error:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from error

    module = import_module(f"{__name__}.{module_name}")
    value = getattr(module, attribute_name)
    globals()[name] = value
    return value

__all__ = [
    "TrafficStateEstimationService",
    "TrafficPredictionEngine",
    "PredictionResult",
    "AIDecisionEngine",
    "SignalDecision",
    "SignalOptimizationEngine",
    "OptimizedSignalPlan",
    "SafetyValidationEngine",
    "SanitizedSignalCommand",
    "MultiIntersectionCoordinator",
    "GreenWaveCorridor",
]
