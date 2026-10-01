import pytest
from src.services.water_waste.engine.leak import LeakDetectionEngine

def test_leak_detection_normal():
    engine = LeakDetectionEngine()
    # 10,000 expected, 10,500 observed. Deviation is 5%. Threshold is 20%.
    is_candidate = engine.detect_leak_candidate(10000.0, 10500.0)
    assert is_candidate is False

def test_leak_detection_anomaly():
    engine = LeakDetectionEngine()
    # 10,000 expected, 13,000 observed. Deviation is 30%.
    is_candidate = engine.detect_leak_candidate(10000.0, 13000.0)
    assert is_candidate is True

def test_leak_detection_zero_expected():
    engine = LeakDetectionEngine()
    # Expected 0 (e.g. night time isolated zone), observed 50 L/h
    is_candidate = engine.detect_leak_candidate(0.0, 50.0)
    assert is_candidate is True
