# AFRM Prototype

## Project Overview

The Aircraft Fuel and Range Management (AFRM) Prototype is a command-line application that takes simulated flight and fuel data, checks it, and calculates the fuel and range figures a crew would use to decide whether a route can be completed. It then compares the predicted fuel at the route endpoint against a project-defined reserve threshold and reports one of three outcomes:

- **Meets simulated criteria**
- **Below simulated threshold**
- **Insufficient fuel to reach endpoint under the model**

The program also compares actual fuel used with planned fuel use over the same interval. Invalid inputs are rejected with clear messages, and no calculations or predictions are shown until the inputs are corrected.

## Scope and Limitations

The AFRM Prototype uses simulated flight and fuel data and is not intended for operational use.

- One simulated aircraft, route and checkpoint
- Constant fuel flow and groundspeed
- A project-defined threshold
- No live data, weather, payload modelling or diversion advice

## Environment

- Windows 11
- Visual Studio Code 1.143.1
- Python 3.11.9
- Git 2.47.1.windows.2 for version control

## Dependencies

- The program itself uses the Python standard library only.
- `pytest` is required to run the tests.

## Setup

1. Clone or download the repository and open the `AFRM Prototype` folder in a terminal.
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.
3. Install the test dependency:
   ```powershell
   python -m pip install pytest
   ```

## Run Instructions

From the top-level `AFRM Prototype` folder:

```powershell
python src/main.py
```

The program prompts for seven values, each shown with its unit:

| Input                    | Unit |
| ------------------------ | ---- |
| Current usable fuel      | kg   |
| Fuel flow                | kg/h |
| Groundspeed              | km/h |
| Remaining route distance | km   |
| Planned fuel use         | kg   |
| Actual fuel used         | kg   |
| Reserve threshold        | kg   |

If any value is missing, non-numeric, negative, or zero where zero is not allowed (fuel flow and groundspeed), the program lists the problems and asks again for only the invalid fields. Results are displayed only once all inputs are valid.

## Test Instructions

From the top-level folder:

```powershell
python -m pytest
```

For a list of every test by name:

```powershell
python -m pytest -v
```

| Test file              | Covers                                                                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `test_validation.py`   | R01 and the validation part of R06: valid dataset, missing, non-numeric, negative, and zero-value inputs               |
| `test_calculations.py` | R02, R03, R04: endurance, range, endpoint fuel, margin, and fuel-use difference, including boundary and negative cases |
| `test_status.py`       | R06: each status outcome and the boundaries at 0 kg and at the threshold                                               |
| `test_ui.py`           | R05: displayed values, units, status, and validation messages                                                          |

## Example Data and Assumptions

### Example dataset

| Input                    | Value    |
| ------------------------ | -------- |
| Current usable fuel      | 1200 kg  |
| Fuel flow                | 200 kg/h |
| Groundspeed              | 250 km/h |
| Remaining route distance | 500 km   |
| Planned fuel use         | 80 kg    |
| Actual fuel used         | 100 kg   |
| Reserve threshold        | 200 kg   |

### Expected results

| Output                     | Calculation                          | Result                     |
| -------------------------- | ------------------------------------ | -------------------------- |
| Total endurance            | fuel / fuel flow                     | 6 h                        |
| Endurance to threshold     | (fuel - threshold) / fuel flow       | 5 h                        |
| Range preserving threshold | endurance to threshold x groundspeed | 1250 km                    |
| Time to route endpoint     | distance / groundspeed               | 2 h                        |
| Fuel required to endpoint  | time to endpoint x fuel flow         | 400 kg                     |
| Predicted fuel at endpoint | fuel - fuel required                 | 800 kg                     |
| Margin vs threshold        | predicted endpoint fuel - threshold  | +600 kg                    |
| Fuel-use difference        | actual - planned                     | +20 kg (more than planned) |
| Status                     |                                      | Meets simulated criteria   |

### Status logic

| Condition                         | Status                                              |
| --------------------------------- | --------------------------------------------------- |
| Predicted endpoint fuel < 0 kg    | Insufficient fuel to reach endpoint under the model |
| 0 kg <= endpoint fuel < threshold | Below simulated threshold                           |
| Endpoint fuel >= threshold        | Meets simulated criteria                            |

An endpoint fuel exactly equal to the threshold meets the criteria. An endpoint fuel of exactly 0 kg with a positive threshold is reported as below the threshold, not insufficient, because the model does not predict running out of fuel before the endpoint.

### Assumptions

- All data is simulated and units are fixed (kg, kg/h, km/h, km, hours).
- Fuel flow and groundspeed are constant for the whole route.
- The 200 kg reserve threshold is a simulated value equal to one hour of flight at the example fuel flow of 200 kg/h. It is not taken from real regulations.
- Fuel flow and groundspeed must be greater than zero, because they are divisors in the calculations.
- Planned and actual fuel use are measured over the same interval.
- If the threshold is above the current fuel, endurance to the threshold and the range are reported as 0 rather than negative values.
- Any invalid input stops all dependent calculations, so no misleading predictions are displayed.
