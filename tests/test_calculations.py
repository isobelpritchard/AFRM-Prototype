from src.models import FlightInputs
from src import calculations as calc

EXAMPLE = FlightInputs(1200, 200, 250, 500, 80, 100, 200)


def test_total_endurance():
    assert calc.total_endurance_h(EXAMPLE) == 6


def test_endurance_to_threshold():
    assert calc.endurance_to_threshold_h(EXAMPLE) == 5


def test_range_preserving_threshold():
    assert calc.range_preserving_threshold_km(EXAMPLE) == 1250


def test_time_to_endpoint():
    assert calc.time_to_endpoint_h(EXAMPLE) == 2