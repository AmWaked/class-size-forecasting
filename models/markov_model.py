"""Four-state Markov chain calculations for course enrollment."""

states = ("CS1", "CS2", "CS3", "Done")

transition_matrix = (
    [0.20, 0.80, 0, 0],
    [0, 0.20, 0.80, 0],
    [0, 0, 0.20, 0.80],
    [0, 0, 0, 1.00]
)


def forecast_enrollment(students, transition_matrix):
    """Project a state vector forward one semester using its transition matrix."""
    if not students or len(transition_matrix) != len(students):
        raise ValueError("The transition matrix must match the enrollment states.")

    next_semester = [0.0] * len(students)
    for state_index, row in enumerate(transition_matrix):
        if len(row) != len(students):
            raise ValueError("The transition matrix must be square.")
        for next_state_index, probability in enumerate(row):
            next_semester[next_state_index] += students[state_index] * probability
    return next_semester