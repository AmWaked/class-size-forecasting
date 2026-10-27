"""Basic tests for model interface compliance."""

import pytest

from models.markov import MarkovModel
from models.markov_model import forecast_enrollment
from models.simulation import SimulationModel


def test_markov_implements_interface():
    model = MarkovModel()
    assert hasattr(model, "fit")
    assert hasattr(model, "predict")


def test_markov_forecasts_each_state_for_multiple_semesters():
    model = MarkovModel()
    model.fit({"CS1": 100, "CS2": 80, "CS3": 50, "Done": 0})

    forecast = model.predict(2)

    assert [(state, semester) for state, semester, _ in forecast] == [
        ("CS1", 1),
        ("CS2", 1),
        ("CS3", 1),
        ("Done", 1),
        ("CS1", 2),
        ("CS2", 2),
        ("CS3", 2),
        ("Done", 2),
    ]
    assert [enrollment for _, _, enrollment in forecast] == pytest.approx(
        [20.0, 96.0, 74.0, 40.0, 4.0, 35.2, 91.6, 99.2]
    )


def test_markov_forecast_preserves_total_enrollment():
    next_semester = forecast_enrollment(
        [100, 80, 50, 0],
        [[0.2, 0.8, 0, 0], [0, 0.2, 0.8, 0], [0, 0, 0.2, 0.8], [0, 0, 0, 1]],
    )

    assert sum(next_semester) == pytest.approx(230)


@pytest.mark.parametrize(
    ("initial_enrollment", "message"),
    [
        ({"CS1": 1, "CS2": 2, "CS3": 3}, "missing states"),
        ({"CS1": -1, "CS2": 2, "CS3": 3, "Done": 0}, "non-negative whole number"),
        ({"CS1": 1.5, "CS2": 2, "CS3": 3, "Done": 0}, "non-negative whole number"),
    ],
)
def test_markov_rejects_invalid_initial_enrollment(initial_enrollment, message):
    with pytest.raises(ValueError, match=message):
        MarkovModel().fit(initial_enrollment)


def test_markov_requires_fit_before_prediction():
    with pytest.raises(ValueError, match="fit"):
        MarkovModel().predict()


def test_simulation_implements_interface():
    model = SimulationModel()
    assert hasattr(model, "fit")
    assert hasattr(model, "predict")


#Verifies that a simple one semester Markov calculation moves students between states using the expected transition rates
def test_markov_single_semester_calculation():
    model = MarkovModel()
    model.fit({"CS1": 100, "CS2": 0, "CS3": 0, "Done": 0})

    forecast = model.predict(1)

    assert [enrollment for _, _, enrollment in forecast] == pytest.approx(
        [20.0, 80.0, 0.0, 0.0]
    )

#Verifies the expected enrollment values for all states after one semester using the current transition matrix
    def test_markov_one_semester_expected_values():
    model = MarkovModel()
    model.fit({"CS1": 100, "CS2": 80, "CS3": 50, "Done": 0})

    forecast = model.predict(1)

    assert [enrollment for _, _, enrollment in forecast] == pytest.approx(
        [20.0, 96.0, 74.0, 40.0]
    )

#Verifies that zero initial enrollment remains zero across multiple forecasted semesters
    def test_markov_zero_enrollment_remains_zero():
    model = MarkovModel()
    model.fit({"CS1": 0, "CS2": 0, "CS3": 0, "Done": 0})

    forecast = model.predict(2)

    assert all(enrollment == 0 for _, _, enrollment in forecast)
