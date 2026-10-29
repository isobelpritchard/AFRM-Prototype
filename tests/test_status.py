from dataclasses import replace

from src.models import FlightInputs
from src.status import FuelStatus, assess_status

# endpoint fuel = 1200 - 400 = 800 kg, threshold 200 kg
EXAMPLE = FlightInputs(1200, 200, 250, 500, 80, 100, 200)


def test_example_meets_criteria():
    assert assess_status(EXAMPLE) == FuelStatus.MEETS_CRITERIA


def test_endpoint_exactly_at_threshold_meets_criteria():
    case = replace(EXAMPLE, reserve_threshold_kg=800)
    assert assess_status(case) == FuelStatus.MEETS_CRITERIA


def test_endpoint_just_below_threshold():
    case = replace(EXAMPLE, reserve_threshold_kg=801)
    assert assess_status(case) == FuelStatus.BELOW_THRESHOLD


def test_endpoint_exactly_zero_is_below_threshold_not_insufficient():
    case = replace(EXAMPLE, current_fuel_kg=400)  # endpoint = 0
    assert assess_status(case) == FuelStatus.BELOW_THRESHOLD


def test_negative_endpoint_is_insufficient():
    case = replace(EXAMPLE, current_fuel_kg=399)  # endpoint = -1
    assert assess_status(case) == FuelStatus.INSUFFICIENT