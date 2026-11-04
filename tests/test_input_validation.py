"""Tests for input validation module."""

import pytest

from app.input_validation import (
    validate_students,
    validate_transition_matrix,
    validate_semesters,
    validate_all,
)

GOOD_MATRIX = [
    [0.20, 0.80, 0, 0],
    [0, 0.20, 0.80, 0],
    [0, 0, 0.20, 0.80],
    [0, 0, 0, 1.00],
]

def test_students_valid_list():
    assert validate_students([100, 80, 50, 0]) is True

def test_students_valid_dict():
    assert validate_students({"CS1": 100, "CS2": 80, "CS3": 50, "Done": 0}) is True

def test_students_valid_tuple():
    assert validate_students((100, 80, 50, 0)) is True

def test_students_wrong_length():
    with pytest.raises(ValueError, match="4 states"):
        validate_students([100, 80, 50])

def test_students_negative():
    with pytest.raises(ValueError, match="cant be negative"):
        validate_students([100, -5, 50, 0])

def test_students_dict_shows_state_name():
    with pytest.raises(ValueError, match="CS2"):
        validate_students({"CS1": 100, "CS2": -5, "CS3": 50, "Done": 0})

def test_students_boolean():
    with pytest.raises(ValueError, match="boolean"):
        validate_students([True, 80, 50, 0])

def test_students_string():
    with pytest.raises(ValueError, match="not a number"):
        validate_students([100, "eighty", 50, 0])

def test_students_nan():
    with pytest.raises(ValueError, match="not finite"):
        validate_students([float("nan"), 80, 50, 0])

def test_students_fractional():
    with pytest.raises(ValueError, match="whole number"):
        validate_students([1.5, 80, 50, 0])

def test_students_wrong_dict_keys():
    with pytest.raises(ValueError, match="states"):
        validate_students({"CS1": 100, "CS2": 80, "CS3": 50, "Wrong": 0})

def test_students_bad_type():
    with pytest.raises(ValueError):
        validate_students("not valid")


def test_matrix_valid():
    assert validate_transition_matrix(GOOD_MATRIX) is True

def test_matrix_tuple():
    t = tuple(tuple(r) for r in GOOD_MATRIX)
    assert validate_transition_matrix(t) is True

def test_matrix_wrong_size():
    with pytest.raises(ValueError, match="4x4"):
        validate_transition_matrix(GOOD_MATRIX[:3])

def test_matrix_short_row():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[1] = [0, 0.20, 0.80]
    with pytest.raises(ValueError, match="4 columns"):
        validate_transition_matrix(bad)

def test_matrix_negative_probability():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[0] = [-0.1, 1.1, 0, 0]
    with pytest.raises(ValueError, match="not a valid probability"):
        validate_transition_matrix(bad)

def test_matrix_bad_row_sum():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[0] = [0.20, 0.79, 0, 0]
    with pytest.raises(ValueError, match="sum to"):
        validate_transition_matrix(bad)

def test_matrix_nan():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[0] = [float("nan"), 0.80, 0, 0]
    with pytest.raises(ValueError, match="not finite"):
        validate_transition_matrix(bad)

def test_matrix_string():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[0] = ["0.2", 0.80, 0, 0]
    with pytest.raises(ValueError, match="not a number"):
        validate_transition_matrix(bad)


def test_semesters_valid():
    assert validate_semesters(1) is True
    assert validate_semesters(20) is True

def test_semesters_zero():
    with pytest.raises(ValueError, match="at least 1"):
        validate_semesters(0)

def test_semesters_over_limit():
    with pytest.raises(ValueError, match="more than 20"):
        validate_semesters(21)

def test_semesters_not_int():
    with pytest.raises(ValueError, match="integer"):
        validate_semesters(3.5)

def test_semesters_boolean():
    with pytest.raises(ValueError, match="boolean"):
        validate_semesters(True)


def test_validate_all_passes():
    assert validate_all([100, 80, 50, 0], GOOD_MATRIX, 3) is True

def test_validate_all_dict():
    d = {"CS1": 100, "CS2": 80, "CS3": 50, "Done": 0}
    assert validate_all(d, GOOD_MATRIX, 3) is True

def test_validate_all_bad_students():
    with pytest.raises(ValueError):
        validate_all([-1, 80, 50, 0], GOOD_MATRIX, 3)

def test_validate_all_bad_matrix():
    bad = [r[:] for r in GOOD_MATRIX]
    bad[0] = [0.5, 0.5, 0.5, 0]
    with pytest.raises(ValueError):
        validate_all([100, 80, 50, 0], bad, 3)

def test_validate_all_bad_semesters():
    with pytest.raises(ValueError):
        validate_all([100, 80, 50, 0], GOOD_MATRIX, 0)
