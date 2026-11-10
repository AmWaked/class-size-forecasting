"""Milestone 2 checks using synthetic enrollment, not historical student data."""

from copy import deepcopy

import numpy as np
import pytest

from app.markov_forecast import (
    build_transition_matrix, courses, passing_rates, predict_enrollment,
)


STARTING_COUNTS = {
    "CIST1400": 100, "CSCI1620": 50, "CSCI2030": 30, "CSCI2040": 40,
    "CSCI2240": 25, "CSCI3320": 20, "CSCI3660": 15, "CSCI3720": 10,
    "CSCI4100": 12, "CSCI4220": 10, "CSCI4830": 8,
}


#swap one rate without touching the rest
def with_first_rate(rate):
    rates = deepcopy(passing_rates)
    rates["CIST1400"]["CSCI1620"] = rate
    return rates


@pytest.mark.parametrize(
    "edited_rate, expected_first, expected_second",
    [(None, (30, 55), (9, 28.5)), (0.50, (20, 65), (4, 29.5))],
    ids=["default-rates", "edited-rate"],
)
def test_four_semester_scenario(edited_rate, expected_first, expected_second):
    rates = passing_rates if edited_rate is None else with_first_rate(edited_rate)
    matrix = build_transition_matrix(rates)
    starting = [STARTING_COUNTS[course] for course in courses]
    forecast = predict_enrollment(starting, matrix, semesters_ahead=4)

    assert forecast.shape == (4, 11)
    pair = [courses.index("CIST1400"), courses.index("CSCI1620")]
    np.testing.assert_allclose(forecast[0, pair], expected_first)
    np.testing.assert_allclose(forecast[1, pair], expected_second)
    np.testing.assert_allclose(forecast.sum(axis=1), [320] * 4)
    assert np.all(forecast >= 0)


def test_default_matrix_assigns_unspent_probability_to_same_course():
    matrix = build_transition_matrix(passing_rates)
    assert matrix.shape == (11, 11)
    np.testing.assert_allclose(matrix.sum(axis=1), 1)
    first = courses.index("CIST1400")
    assert matrix[first, first] == pytest.approx(0.30)
    #terminal course has nowhere to go so diagonal should be 1
    terminal = courses.index("CSCI4830")
    assert matrix[terminal, terminal] == 1


def test_outgoing_total_over_one_identifies_course():
    #0.80 to CSCI1620 + 0.30 to CSCI2030 = 1.10
    with pytest.raises(ValueError, match="CIST1400"):
        build_transition_matrix(with_first_rate(0.80))


@pytest.mark.parametrize("rate", [-0.1, 1.1, np.nan, np.inf, -np.inf, True, None])
def test_invalid_probability_identifies_course_pair(rate):
    with pytest.raises(ValueError, match="CIST1400.*CSCI1620"):
        build_transition_matrix(with_first_rate(rate))
