import math
from src.models import FlightInputs

# field name -> (label, unit, must_be_greater_than_zero)
FIELDS = {
    "current_fuel_kg":      ("Current usable fuel", "kg", False),
    "fuel_flow_kg_h":       ("Fuel flow", "kg/h", True),
    "groundspeed_kmh":      ("Groundspeed", "km/h", True),
    "route_distance_km":    ("Remaining route distance", "km", False),
    "planned_fuel_kg":      ("Planned fuel use", "kg", False),
    "actual_fuel_kg":       ("Actual fuel used", "kg", False),
    "reserve_threshold_kg": ("Reserve threshold", "kg", False),
}


def validate_inputs(raw: dict):
    """Validate raw (string) inputs.

    Returns (FlightInputs, {}) if all valid,
    or (None, {field: error message}) if any are invalid.
    """
    errors = {}
    values = {}

    for field, (label, unit, must_be_positive) in FIELDS.items():
        text = str(raw.get(field, "")).strip()

        if text == "":
            errors[field] = f"{label} is missing."
            continue
        try:
            value = float(text)
        except ValueError:
            errors[field] = f"{label} must be a number ({unit})."
            continue
        if not math.isfinite(value):
            errors[field] = f"{label} must be a finite number."
            continue
        if value < 0:
            errors[field] = f"{label} cannot be negative."
            continue
        if must_be_positive and value == 0:
            errors[field] = f"{label} must be greater than zero."
            continue

        values[field] = value

    if errors:
        return None, errors
    return FlightInputs(**values), {}