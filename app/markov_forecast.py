import numpy as np

#List of Computer Science courses included in the model
courses = ['CIST1400', 'CSCI1620', 'CSCI2030', 'CSCI2040',
           'CSCI2240', 'CSCI3320', 'CSCI3660', 'CSCI3720',
           'CSCI4100', 'CSCI4220', 'CSCI4830']

#course prerequisite relationships
prerequisites = {
    'CSCI1620': ['CIST1400'],
    'CSCI2030': ['CIST1400'],
    'CSCI2040': ['CSCI1620'],
    'CSCI2240': ['CSCI1620'],
    'CSCI3320': ['CSCI2030', 'CSCI2040'],
    'CSCI3660': ['CSCI3320'],
    'CSCI3720': ['CSCI2030'],
    'CSCI4100': ['CSCI3320'],
    'CSCI4220': ['CSCI3320', 'CSCI3660'],
    'CSCI4830': ['CSCI3320']
}

#Hypothetical progression probabilities used to test the model
#These are estimates, not probabilities calculated from historical data

passing_rates = {
    'CIST1400':{
        'CSCI1620': 0.40,
        'CSCI2030': 0.30
    },
    'CSCI1620':{
            'CSCI2040': 0.40,
            'CSCI2240': 0.30
        },
    'CSCI2030':{
            'CSCI3320': 0.40,
            'CSCI3720': 0.30
    },
    'CSCI2040':{
        'CSCI3320': 0.40
    },
    'CSCI3320':{
        'CSCI3660': 0.40,
        'CSCI4100': 0.30,
        'CSCI4220': 0.20,
        'CSCI4830': 0.10
    },
    'CSCI3660':{
        'CSCI4220': 0.70
    }
}

#dynamically generate the markov transition matrix
def build_transition_matrix(rates):
    #create an 11*11 matrix filled with zeros
    numpy_matrix = np.zeros((len(courses), len(courses)))

    #Find course relationships and assign probabilities
    for course in courses:
        for next_course in courses:
            if course in prerequisites.get(next_course, []):
                current_index = courses.index(course)
                next_index = courses.index(next_course)

                numpy_matrix[current_index, next_index] =rates.get(
                    course, {}
                ).get(next_course, 0.0)

    # CALCULATE THE PROBABILITY OF REMAINING IN  EACH COURSE
    # The remaining probability represents staying in the same course state
    remaining_probability = 1 - np.sum(numpy_matrix, axis=1)

    #check that no course has probabilities totaling more than 100%
    if np.any(remaining_probability < -1e-9):
        raise ValueError("Course transition probabilities cannot exceed 1.")

    # Replace small floating-point rounding errors with zero
    remaining_probability = np.where(
        np.isclose(remaining_probability, 0),
        0,
        remaining_probability
    )

    #fill the diagonal of the transmission matrix
    np.fill_diagonal(numpy_matrix, remaining_probability)
    return numpy_matrix

#forecast enrollment using the Markov transition matrix
def predict_enrollment(students, matrix, semesters_ahead=1):
    #make a copy of the enrollment data
    forecast = np.array(students, dtype=float)

    #calculate enrollment for each future semester
    predictions = []

    for semester in range(1, semesters_ahead + 1):
        forecast = forecast @ matrix
        predictions.append(forecast.copy())

    return np.array(predictions)

