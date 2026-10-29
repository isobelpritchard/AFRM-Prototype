from enum import Enum

from models import FlightInputs
import calculations as calc


class FuelStatus(Enum):
    INSUFFICIENT = "Insufficient fuel to reach endpoint under the model"
    BELOW_THRESHOLD = "Below simulated threshold"
    MEETS_CRITERIA = "Meets simulated criteria"


def assess_status(i: FlightInputs) -> FuelStatus:
    endpoint = calc.endpoint_fuel_kg(i)

    if endpoint < 0:
        return FuelStatus.INSUFFICIENT
    if endpoint < i.reserve_threshold_kg:
        return FuelStatus.BELOW_THRESHOLD
    return FuelStatus.MEETS_CRITERIA