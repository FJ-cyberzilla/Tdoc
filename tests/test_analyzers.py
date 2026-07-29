"""
Tests for individual analyzer components.
"""

from src.services.analyzers.activity import ActivityAnalyzer
from src.services.analyzers.environment import EnvironmentAnalyzer
from src.services.analyzers.orientation import OrientationAnalyzer


def test_activity_analyzer():
    analyzer = ActivityAnalyzer()

    # Stationary
    data = {"Accelerometer": {"values": [0, 0, 9.8]}}
    res = analyzer.analyze(data)
    assert res["status"] == "STATIONARY"

    # Running
    data = {"Accelerometer": {"values": [10, 10, 10]}}
    res = analyzer.analyze(data)
    assert res["status"] == "RUNNING"


def test_environment_analyzer():
    analyzer = EnvironmentAnalyzer()
    data = {
        "Magnetometer": {"values": [1.0, 2.0, 3.0]},
        "Hall IC": {"values": [0.0]},
        "Light": {"values": [300.0]},
    }
    res = analyzer.analyze(data)
    assert res["Magnetometer"]["values"] == [1.0, 2.0, 3.0]
    assert res["Hall IC"]["values"] == [0.0]
    assert res["light"] == 300.0


def test_orientation_analyzer():
    analyzer = OrientationAnalyzer()

    # Stable
    data = {"Gyroscope": {"values": [0.1, 0.1, 0.1]}}
    res = analyzer.analyze(data)
    assert res["status"] == "STABLE"

    # Rotating
    data = {"Gyroscope": {"values": [1.0, 0.1, 0.1]}}
    res = analyzer.analyze(data)
    assert res["status"] == "ROTATING"
