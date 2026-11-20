import numpy as np

#Names of the 9 forecast output columns
forecast_states = [
    "CS1", "CS2", "CS3",
    "CS4", "CS6",
    "CS5", "CS7",
    "Done CS6", "Done CS7",
]
#original four-state example
states = ["CS1", "CS2", "CS3", "Done"]

transition_matrix = np.array([
    [0.25, 0.75, 0.00, 0.00],
    [0.00, 0.30, 0.70, 0.00],
    [0.00, 0.00, 0.20, 0.80],
    [0.00, 0.00, 0.00, 1.00]
])

#Starting enrollment
students = np.array([100, 100, 100, 0])

#first branch: CS4 -> CS6 -> Done
branch1_states = ["CS4", "CS6","Done"]

branch1_matrix = np.array([
    [0.40, 0.60, 0.00],
    [0.00, 0.10, 0.90],
    [0.00, 0.00, 1.00]
])

#Second branch: CS5 -> CS7 -> Done
branch2_states = ["CS5", "CS7", "Done"]

branch2_matrix = np.array([
    [0.15, 0.85, 0.00],
    [0.00, 0.20, 0.80],
    [0.00, 0.00, 1.00]
])


#forecast 4 semesters automatically
def forecast_branches(semesters):
    """Return a forecast array with 9 columns for the requested semesters"""

    original = students.copy()
    branch1 = np.zeros(3)


    branch2 = np.zeros(3)

    forecast_results = []

    for semester in range(1, semesters +1 ):

        #Advance the original chain
        original_next = original @ transition_matrix

        #count only New student completing CS3
        new_completions = original_next[3] - original[3]

        #advance students already in the branches
        branch1 = branch1 @ branch1_matrix
        branch2 = branch2 @ branch2_matrix

        #Add new students to both branches
        branch1[0] += new_completions
        branch2[0] += new_completions

        #update the original chain
        original = original_next

        combined_forecast = np.concatenate((
            original[:3],
            branch1[:2],
            branch2[:2],
            branch1[2:],
            branch2[2:]
        ))

        forecast_results.append(combined_forecast.copy())

    return np.array(forecast_results)
#run the forecast for 4 semesters
if __name__ == "__main__":
    results = forecast_branches(4)
    print("Saved semesters:", len(results))