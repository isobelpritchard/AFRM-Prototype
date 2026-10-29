import builtins
from dataclasses import replace

import pytest

import main as app
import ui
from models import FlightInputs

EXAMPLE = FlightInputs(1200, 200, 250, 500, 80, 100, 200)


def test_results_show_values_units_and_status(capsys):
    ui.show_results(EXAMPLE)
    out = capsys.readouterr().out
    for text in ["1200.0 kg", "200.0 kg/h", "250.0 km/h", "500.0 km",
                 "1250.0 km", "+600.0 kg", "+20.0 kg",
                 "Meets simulated criteria"]:
        assert text in out


@pytest.mark.parametrize("case, expected", [
    (EXAMPLE, "Meets simulated criteria"),
    (replace(EXAMPLE, reserve_threshold_kg=1000), "Below simulated threshold"),
    (replace(EXAMPLE, current_fuel_kg=300), "Insufficient fuel"),
])
def test_each_status_is_displayed(capsys, case, expected):
    ui.show_results(case)
    assert expected in capsys.readouterr().out


def test_invalid_input_shows_message_and_no_results_until_corrected(monkeypatch, capsys):
    answers = iter(["1200", "200", "0", "500", "80", "100", "200",  # zero groundspeed
                    "250"])                                          # corrected value
    monkeypatch.setattr(builtins, "input", lambda _="": next(answers))
    app.main()
    out = capsys.readouterr().out
    assert out.index("Groundspeed must be greater than zero") < out.index("AFRM RESULTS")
    assert out.count("AFRM RESULTS") == 1