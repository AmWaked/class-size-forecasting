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

    # Check that the matrix matches the number of states
    if not students or len(transition_matrix) != len(students):
        raise ValueError("The transition matrix must match the enrollment states.")

    # Check that the transition matrix is square
    for row in transition_matrix:
        if len(row) != len(students):
            raise ValueError("The transition matrix must be square.")

    # Convert the student list into a NumPy array
    student_vector = np.array(students)

    # Convert the transition matrix into a NumPy array
    transition_array = np.array(transition_matrix)

    # Multiply the student vector by the transition matrix
    next_semester = student_vector @ transition_array

    # Return the predicted enrollment as a Python list
    return next_semester.tolist()
