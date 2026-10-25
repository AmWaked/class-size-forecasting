#Input Validation Module

import math

STATES = ["CS1", "CS2", "CS3", "Done"]

def validate_students(students):
    """check that enrollment numbers make sense before passing to model"""
    if isinstance(students, dict):
        if set(students.keys()) != set(STATES):
            raise ValueError(f"need exactly these states: {set(STATES)}, got {set(students.keys())}")
        values = [students[k] for k in STATES]
        labels = STATES
    elif isinstance(students, (list, tuple)):
        values = list(students)
        labels = STATES
        if len(values) != 4:
            raise ValueError("need exactly 4 states (CS1, CS2, CS3, Done)")
    else:
        raise ValueError("students must be a list, tuple, or dict")

    for i, s in enumerate(values):
        name = labels[i]
        if isinstance(s, bool):
            raise ValueError(f"{name} enrollment is a boolean not a number")
        if not isinstance(s, (int, float)):
            raise ValueError(f"{name} enrollment is not a number")
        #catch ints that overflow when converting to float
        try:
            ok = math.isfinite(s)
        except (OverflowError, TypeError):
            raise ValueError(f"{name} enrollment value is too large")
        if not ok:
            raise ValueError(f"{name} enrollment is not finite")
        if s < 0:
            raise ValueError(f"{name} enrollment cant be negative")
        if isinstance(s, float) and s != int(s):
            raise ValueError(f"{name} enrollment must be a whole number")
    return True


def validate_transition_matrix(matrix):
    """make sure transition matrix is valid"""
    if not isinstance(matrix, (list, tuple)):
        raise ValueError("matrix must be a list or tuple of rows")
    if len(matrix) != 4:
        raise ValueError("matrix must be 4x4")
    for i, row in enumerate(matrix):
        if not isinstance(row, (list, tuple)):
            raise ValueError(f"row {i} is not a list or tuple")
        if len(row) != 4:
            raise ValueError(f"row {i} doesnt have 4 columns")
        for j, val in enumerate(row):
            if isinstance(val, bool):
                raise ValueError(f"matrix[{i}][{j}] is a boolean not a number")
            if not isinstance(val, (int, float)):
                raise ValueError(f"matrix[{i}][{j}] is not a number")
            try:
                ok = math.isfinite(val)
            except (OverflowError, TypeError):
                raise ValueError(f"matrix[{i}][{j}] is too large")
            if not ok:
                raise ValueError(f"matrix[{i}][{j}] is not finite")
            if val < 0 or val > 1:
                raise ValueError(f"matrix[{i}][{j}] is not a valid probability")
        row_sum = sum(row)
        if abs(row_sum - 1.0) > 1e-9:
            raise ValueError(f"row {i} probabilities sum to {row_sum}, should be 1.0")
    return True


def validate_semesters(semesters):
    """check semesters ahead parameter"""
    if isinstance(semesters, bool):
        raise ValueError("semesters must be an integer not a boolean")
    if not isinstance(semesters, int):
        raise ValueError("semesters must be an integer")
    if semesters < 1:
        raise ValueError("need at least 1 semester to forecast")
    if semesters > 20:
        raise ValueError("cant forecast more than 20 semesters out")
    return True


def validate_all(students, transition_matrix, semesters):
    """run all checks before forecasting.
    returns True if everything passes otherwise raises ValueError"""
    validate_students(students)
    validate_transition_matrix(transition_matrix)
    validate_semesters(semesters)
    return True


#quick test
if __name__ == "__main__":
    students = [100, 80, 50, 0]
    matrix = [
        [0.20, 0.80, 0, 0],
        [0, 0.20, 0.80, 0],
        [0, 0, 0.20, 0.80],
        [0, 0, 0, 1.00]
    ]
    print("validating...")
    validate_all(students, matrix, 3)
    print("all checks passed")

    #test with dict input like the gui uses
    student_dict = {"CS1": 100, "CS2": 80, "CS3": 50, "Done": 0}
    validate_students(student_dict)
    print("dict input works")

    #test with tuple matrix like the repo uses
    tuple_matrix = tuple(tuple(r) for r in matrix)
    validate_transition_matrix(tuple_matrix)
    print("tuple matrix works")
