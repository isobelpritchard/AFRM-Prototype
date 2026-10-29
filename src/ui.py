from models import FlightInputs
from validation import FIELDS
import calculations as calc
from status import assess_status


def ask(field: str) -> str:
    label, unit, _ = FIELDS[field]
    return input(f"{label} ({unit}): ")


def show_errors(errors: dict) -> None:
    print("\nInvalid inputs - please correct:")
    for message in errors.values():
        print(f"  ! {message}")
    print()


def _fuel_use_text(difference: float) -> str:
    if difference > 0:
        return f"{difference:+.1f} kg (more fuel used than planned)"
    if difference < 0:
        return f"{difference:+.1f} kg (less fuel used than planned)"
    return "0.0 kg (as planned)"


def show_results(i: FlightInputs) -> None:
    print("\nAFRM RESULTS (simulated data)")

    print("\nInputs")
    print(f"  Current usable fuel:      {i.current_fuel_kg:.1f} kg")
    print(f"  Fuel flow:                {i.fuel_flow_kg_h:.1f} kg/h")
    print(f"  Groundspeed:              {i.groundspeed_kmh:.1f} km/h")
    print(f"  Remaining route distance: {i.route_distance_km:.1f} km")
    print(f"  Planned fuel use:         {i.planned_fuel_kg:.1f} kg")
    print(f"  Actual fuel used:         {i.actual_fuel_kg:.1f} kg")
    print(f"  Reserve threshold:        {i.reserve_threshold_kg:.1f} kg")

    print("\nEndurance and range")
    print(f"  Total endurance:              {calc.total_endurance_h(i):.2f} h")
    print(f"  Endurance to threshold:       {calc.endurance_to_threshold_h(i):.2f} h")
    print(f"  Range preserving threshold:   {calc.range_preserving_threshold_km(i):.1f} km")
    print(f"  Time to route endpoint:       {calc.time_to_endpoint_h(i):.2f} h")

    print("\nEndpoint fuel")
    print(f"  Fuel required to endpoint:    {calc.fuel_required_kg(i):.1f} kg")
    print(f"  Predicted fuel at endpoint:   {calc.endpoint_fuel_kg(i):.1f} kg")
    print(f"  Margin vs threshold:          {calc.margin_kg(i):+.1f} kg")

    print("\nFuel use comparison")
    print(f"  Actual - planned:             {_fuel_use_text(calc.fuel_use_difference_kg(i))}")

    print(f"\nSTATUS: {assess_status(i).value}")