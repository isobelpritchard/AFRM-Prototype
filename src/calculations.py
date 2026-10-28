from src.models import FlightInputs


def total_endurance_h(i: FlightInputs) -> float:
    return i.current_fuel_kg / i.fuel_flow_kg_h


def endurance_to_threshold_h(i: FlightInputs) -> float:
    return (i.current_fuel_kg - i.reserve_threshold_kg) / i.fuel_flow_kg_h


def range_preserving_threshold_km(i: FlightInputs) -> float:
    return endurance_to_threshold_h(i) * i.groundspeed_kmh


def time_to_endpoint_h(i: FlightInputs) -> float:
    return i.route_distance_km / i.groundspeed_kmh

def fuel_required_kg(i: FlightInputs) -> float:
    return time_to_endpoint_h(i) * i.fuel_flow_kg_h


def endpoint_fuel_kg(i: FlightInputs) -> float:
    return i.current_fuel_kg - fuel_required_kg(i)


def margin_kg(i: FlightInputs) -> float:
    """Positive = above threshold, negative = below threshold."""
    return endpoint_fuel_kg(i) - i.reserve_threshold_kg