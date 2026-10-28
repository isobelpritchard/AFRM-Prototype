from dataclasses import dataclass


@dataclass(frozen=True)
class FlightInputs:
    current_fuel_kg: float
    fuel_flow_kg_h: float
    groundspeed_kmh: float
    route_distance_km: float
    planned_fuel_kg: float
    actual_fuel_kg: float
    reserve_threshold_kg: float