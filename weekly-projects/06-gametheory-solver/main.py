import pulp
from pulp import *
import numpy as np

def row_player(payoff: np.array):

    prob = LpProblem("game", LpMaximize)

    col_count = payoff.shape[1]
    row_count = payoff.shape[0]

    x_list = range(row_count)

    lp_x_vars = pulp.LpVariable.dicts("x", x_list, 0)

    x_row = list(lp_x_vars.values())
    x_row = np.array(x_row)

    v = LpVariable("v")

    prob += v


    for j in range(col_count):
        sum_ = [lp_x_vars[i] * -payoff[i][j] for i in range(row_count)]# make row negative
        prob += lpSum(sum_+ [v]) <= 0


    prob += lpSum(x_row) == 1


    status = prob.solve()


    return lp_x_vars, pulp.value(prob.objective)

def col_player(payoff: np.array):

    prob = LpProblem("game", LpMinimize)

    col_count = payoff.shape[1]
    row_count = payoff.shape[0]

    y_list = range(row_count)

    lp_y_vars = pulp.LpVariable.dicts("y", y_list, 0)

    y_row = list(lp_y_vars.values())
    y_row = np.array(y_row)

    u = LpVariable("u")

    prob += u


    for j in range(col_count):
        sum_ = [lp_y_vars[i] * -payoff[i][j] for i in range(row_count)]# make row negative
        prob += lpSum(sum_+ [u]) >= 0


    prob += lpSum(y_row) == 1


    status = prob.solve()

    return lp_y_vars, pulp.value(prob.objective)


def solve_game(row_player_payoff: np.array):

    row_strat, row_val = row_player(row_player_payoff)


    col_strat, col_val = col_player(row_player_payoff.T)


    print("ROW PLAYER:")
    for i, var in row_strat.items():
        print(f"{var}: {var.value()}")
    print("")
    print("COL PLAYER:")
    for i, var in col_strat.items():
        print(f"{var}: {var.value()}")


    print(f"Optimal is {row_val}, {col_val}")


    if row_val == col_val:
        if row_val < 0:
            print("Row player has the advantage!")
        elif row_val > 0:
            print("Col player has the advantage!")
        else:
            print("Equal game!")
    else:
        if row_val > col_val:
            print("Row player has the advantage!")
        else:
            print("Col player has the advantage!")



rps = np.array([
    [0,1,-1],
    [-1,0,1],
    [1,-1,0]
])

prisoner_dilemma = np.array([
    [-1,-5],
    [0,-3]
])

coin = np.array([
    [5,-5],
    [-10,10]
])

solve_game(prisoner_dilemma)