"""Basic tests for model interface compliance."""

import pytest

from models.markov import MarkovModel
from models.markov_model import forecast_enrollment, transition_matrix
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
    "transition_matrix",
    [
        [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[-0.1, 1.1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[0.2, 0.7, 0, 0], [0, 0.2, 0.8, 0], [0, 0, 0.2, 0.8], [0, 0, 0, 1]],
        [[float("nan"), 0.8, 0, 0], [0, 0.2, 0.8, 0], [0, 0, 0.2, 0.8], [0, 0, 0, 1]],
    ],
)
def test_markov_forecast_rejects_invalid_transition_matrix(transition_matrix):
    with pytest.raises(ValueError):
        forecast_enrollment([100, 80, 50, 0], transition_matrix)


@pytest.mark.parametrize(
    "students",
    [[100, -1, 50, 0], [100, float("nan"), 50, 0], [[100, 80], [50, 0]]],
)
def test_markov_forecast_rejects_invalid_enrollment_vector(students):
    with pytest.raises(ValueError):
        forecast_enrollment(students, transition_matrix)


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
