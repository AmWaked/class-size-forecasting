"""Four-state Markov chain calculations for course enrollment."""

import numpy as np

states = ("CS1", "CS2", "CS3", "Done")

transition_matrix = (
    [0.20, 0.80, 0, 0],
    [0, 0.20, 0.80, 0],
    [0, 0, 0.20, 0.80],
    [0, 0, 0, 1.00]
)


def forecast_enrollment(students, transition_matrix):
    """Forecast next-semester enrollment using NumPy."""

    try:
        student_vector = np.asarray(students, dtype=float)
        transition_array = np.asarray(transition_matrix, dtype=float)
    except (TypeError, ValueError):
        raise ValueError("Enrollment and transition probabilities must be numeric.") from None

    if student_vector.ndim != 1 or student_vector.size == 0:
        raise ValueError("Enrollment must contain one value per state.")
    if not np.all(np.isfinite(student_vector)) or np.any(student_vector < 0):
        raise ValueError("Enrollment must contain finite, non-negative values.")

    state_count = student_vector.size
    if transition_array.shape != (state_count, state_count):
        raise ValueError("The transition matrix must match the enrollment states.")

    if not np.all(np.isfinite(transition_array)) or np.any(transition_array < 0) or np.any(transition_array > 1):
        raise ValueError("Transition probabilities must be finite values between 0 and 1.")
    if not np.allclose(transition_array.sum(axis=1), 1.0):
        raise ValueError("Each transition matrix row must sum to 1.")

    next_semester = student_vector @ transition_array
    return next_semester.tolist()
