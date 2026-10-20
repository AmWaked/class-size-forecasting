#Class Size Forecasting - Code Milestone 1
#four-state Markov Chain Model

states = ["CS1", "CS2", "CS3", "Done"]
#print(states)

# store the current number of students in each state: CS1,CS2,CS3, and Done.
students = [100, 80, 50, 0]
#print(students)

#Store the probabilities of students moving between courses each semester
transition_matrix = [
    [0.20, 0.80, 0, 0],
    [0, 0.20, 0.80, 0],
    [0, 0, 0.20, 0.80],
    [0, 0, 0, 1.00]
]
#print(transition_matrix)

def forecast_enrollment(students, transition_matrix):

    #students remaining in CS1 next semester
    remaining_in_cs1 = students[0] * transition_matrix[0][0]
    
    #students moving from CS1 to CS2 
    moving_to_cs2 = students[0] * transition_matrix[0][1]
    #print(moving_to_cs2, remaining_in_cs1)

    #students remaining in CS2 next semester
    remaining_in_cs2 = students[1] * transition_matrix[1][1]
    
    #total predicted CS2 enrollment
    cs2_next = remaining_in_cs2 + moving_to_cs2
    #print(remaining_in_cs2, cs2_next)

    #number of students moving from CS2 to CS3 next semester
    moving_to_cs3 = students[1] * transition_matrix[1][2]
    
    #students remainig in cs3 next semester
    remaining_in_cs3 = students[2] * transition_matrix[2][2]
    
    #total predicted CS3 enrollment for next semester
    cs3_next = moving_to_cs3 + remaining_in_cs3
    
    #print(moving_to_cs3)
    #print(remaining_in_cs3)
    #print(cs3_next)

    #students moving from CS3 to Done next semester
    moving_to_done = students[2] * transition_matrix[2][3]
    
    #Total students in the Done state next semester
    done_next = moving_to_done + students[3]
    
    #print(moving_to_done)
    #print(done_next)

    #predicted enrollment for all four states next semester
    next_semester = [remaining_in_cs1, cs2_next, cs3_next, done_next]

    #total number of students predicted for next semester
    #total = sum(next_semester)
    
    #print(total)
    
    return(next_semester)