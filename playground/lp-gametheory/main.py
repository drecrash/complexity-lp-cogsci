import pulp
from pulp import *
import numpy as np

"""
Players A and B each pick a number between 1 and 100. The game is a
draw if both players pick the same number. Otherwise, the player who
picks the smaller number wins unless that smaller number is one less than
the opponent's number, in which case the opponent wins. Find the optimal
strategy for this game.
"""

def eleven_two(N):

    prob = LpProblem("game", LpMaximize)

    payoff = []

    for i in range(N):
        row = []
        for j in range(N):
            val = 0
            if (j < i):
                if (j + 1) == i:
                    val = -1
                else:
                    val = 1
            elif (i<j):
                if (i+1) == j:
                    val = 1
                else:
                    val = -1
                
            row.append(val)

        payoff.append(row)


    payoff = np.array(payoff)


    x_list = range(N)

    lp_x_vars = pulp.LpVariable.dicts("x", x_list, 0)

    x_row = list(lp_x_vars.values())
    x_row = np.array(x_row)

    #x_vars_col_vector = np.atleast_2d(x_row).T # https://stackoverflow.com/questions/36384760/transforming-a-row-vector-into-a-column-vector-in-numpy

    #Ax = np.dot(payoff, x_vars_col_vector)

    v = LpVariable("v")

    prob += v


    for i in range(N):
        sum_ = [lp_x_vars[j] * -payoff[i][j] for j in range(N)]# make row negative
        prob += lpSum(sum_+ [v]) <= 0

    # for row in Ax:
    #     prob += lpSum([-row[0], v]) <= 0 # make row negative

    prob += lpSum(x_row) == 1


    status = prob.solve()

    print(LpStatus[status])

    for i, var in lp_x_vars.items():
        print(f"{var}: {var.value()}")
    print(f"\nOptimal:{pulp.value(prob.objective)}")


    
def eleven_three():
    matrix = np.array([
        [-6, 2, -4, -7, -5],
        [0,4,-2,-9,-1],
        [-7,3,-3,-8,-2],
        [2,-3,6,0,3]
        ])


    matrix = np.array([
        [-6, 2, -4, -5],
        [0,4,-2,-1],
        [2,-3,6,3]
        ])



    def check_dominance(matrix, max_):
        for row, row_vals in enumerate(matrix):
            if row < len(matrix)-1:
                dominant = True
                for col, col_val in enumerate(matrix[row]):
                    
                    if (max_ and col_val < matrix[row+1][col]):
                        dominant = False
                    elif ((not max_) and col_val > matrix[row+1][col]):
                        dominant = False

                if (dominant and max_):
                    print(f"{row} is dominant to {row+1} (Remove row {row+1})")

                if (dominant and not max_):
                    print(f"{row} dominates {row+1} (Remove col {row})")

    print("Rows:")
    check_dominance(matrix,True)
    print("Columns:")
    check_dominance(matrix.transpose(),False)




#eleven_two(5)
eleven_three()