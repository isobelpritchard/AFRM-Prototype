from src.validation import validate_inputs

VALID = {
    "current_fuel_kg": "1200", "fuel_flow_kg_h": "200",
    "groundspeed_kmh": "250", "route_distance_km": "500",
    "planned_fuel_kg": "80", "actual_fuel_kg": "100",
    "reserve_threshold_kg": "200",
}


def test_valid_dataset_accepted():
    inputs, errors = validate_inputs(VALID)
    assert errors == {}
    assert inputs.current_fuel_kg == 1200


def test_missing_input_rejected():
    raw = {**VALID, "groundspeed_kmh": ""}
    inputs, errors = validate_inputs(raw)
    assert inputs is None and "groundspeed_kmh" in errors


def test_negative_fuel_rejected():
    _, errors = validate_inputs({**VALID, "current_fuel_kg": "-5"})
    assert "current_fuel_kg" in errors


def test_zero_groundspeed_rejected():
    _, errors = validate_inputs({**VALID, "groundspeed_kmh": "0"})
    assert "groundspeed_kmh" in errors


def test_zero_fuel_flow_rejected():
    _, errors = validate_inputs({**VALID, "fuel_flow_kg_h": "0"})
    assert "fuel_flow_kg_h" in errors


def test_non_numeric_rejected():
    _, errors = validate_inputs({**VALID, "fuel_flow_kg_h": "abc"})
    assert "fuel_flow_kg_h" in errors