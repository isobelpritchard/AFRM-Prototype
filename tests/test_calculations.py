from src.models import FlightInputs
from src import calculations as calc
import pytest
from dataclasses import replace

EXAMPLE = FlightInputs(1200, 200, 250, 500, 80, 100, 200)


def test_total_endurance():
    assert calc.total_endurance_h(EXAMPLE) == 6


def test_endurance_to_threshold():
    assert calc.endurance_to_threshold_h(EXAMPLE) == 5


def test_range_preserving_threshold():
    assert calc.range_preserving_threshold_km(EXAMPLE) == 1250


def test_time_to_endpoint():
    assert calc.time_to_endpoint_h(EXAMPLE) == 2

def test_fuel_required():
    assert calc.fuel_required_kg(EXAMPLE) == pytest.approx(400)


def test_endpoint_fuel():
    assert calc.endpoint_fuel_kg(EXAMPLE) == pytest.approx(800)


def test_margin_above_threshold():
    assert calc.margin_kg(EXAMPLE) == pytest.approx(600)


def test_margin_equal_to_threshold():
    case = replace(EXAMPLE, reserve_threshold_kg=800)
    assert calc.margin_kg(case) == pytest.approx(0)


def test_margin_below_threshold():
    case = replace(EXAMPLE, reserve_threshold_kg=1000)
    assert calc.margin_kg(case) == pytest.approx(-200)


def test_negative_endpoint_fuel():
    case = replace(EXAMPLE, current_fuel_kg=300)
    assert calc.endpoint_fuel_kg(case) == pytest.approx(-100)
    assert calc.margin_kg(case) == pytest.approx(-300)    