import random
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt
ITERATIONS = 100000

def gen_series(iterations, initial=0, mean=0, var=1):

    series = [initial]

    for i in range(1,iterations):
        new = series[i-1] + np.random.normal(loc=mean, scale=var)
        series.append(new)

    return series

"""
This function calculates the absolute value of the difference between the series value at (t + time step) and the value at (t) 
for every value of t.
It then raises this difference to the power of q before appending it to a list of total differences.
This list is then averaged to return <|x_{t+tau} - x_t|^q>
"""

def calc_avg_diff(q, tau, iterations, series):
    diffs = []

    for t in range(iterations):
        jump = t + tau
        if jump >= iterations:
            break
        diff = abs(series[jump] - series[t])
        diff = math.pow(diff, q)
        diffs.append(diff)


    return statistics.mean(diffs)


"""
This function generates sample data that can be used to approximate V(tau).
It finds V(tau) for varying values of tau (0 through 1000 on a log scale).

"""
def generate_V_data(series, q, iterations):
    taus = np.logspace(0,3,100,dtype=int)
    result = {}

    for tau in taus:
        result[tau] = calc_avg_diff(q, tau, iterations, series)

    return result

"""
This function will use the VData generated in the above function and find a linear fit 
for the data on a logarithmic scale.
The slope can then be extracted to calculate 

"""
def plot_for_q(series, q):
    vdata = generate_V_data(series, q, ITERATIONS)

    taus = list(vdata.keys())
    vs = list(vdata.values())

    slope, intercept = np.polyfit(np.log(taus), np.log(vs),1)
    H = slope / q

    print(f"H({q})={H}")
    plt.plot(taus, vs,label=f"q: {q} - H: {round(H,5)}")



series = gen_series(ITERATIONS)

q_list = range(1,6)
for q in q_list:
    plot_for_q(series,q)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Tau")
plt.ylabel("V(tau)")
plt.legend()
plt.show()