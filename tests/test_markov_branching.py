"""Tests for the Milestone 3 branching Markov forecast."""

import numpy as np
import pytest

from models.markov_branching_practice import forecast_branches, forecast_states


EXPECTED_STATES = [
    "CS1",
    "CS2",
    "CS3",
    "CS4",
    "CS6",
    "CS5",
    "CS7",
    "Done CS6",
    "Done CS7",
]


# Verifies that forecast values correspond to the correct course labels.
def test_branching_forecast_state_labels():
    assert forecast_states == EXPECTED_STATES


# Verifies that the forecast returns one row per requested semester
# and nine forecast values per row.
@pytest.mark.parametrize("semesters", [1, 4, 12])
def test_branching_forecast_dimensions(semesters):
    result = forecast_branches(semesters)

    assert result.shape == (semesters, 9)


# Verifies the expected calculations for the first two semesters.
def test_branching_forecast_expected_values():
    result = forecast_branches(4)

    expected = np.array(
        [
            [25, 105, 90, 80, 0, 80, 0, 0, 0],
            [6.25, 50.25, 91.5, 104, 48, 84, 68, 0, 0],
        ]
    )

    np.testing.assert_allclose(result[:2], expected)


# Verifies that forecast calculations do not produce
# negative, infinite, or missing enrollment values.
def test_branching_forecast_values_are_valid():
    result = forecast_branches(12)

    assert np.all(np.isfinite(result))
    assert np.all(result >= 0)