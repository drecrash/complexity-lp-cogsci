import numpy as np
import json
import matplotlib.pyplot as plt

V = 4
C = 6
INITIAL_HAWK_FRACTION = 0.01

# Hawk fitness
def get_fh(V,C,x):
    return x*(V-C)/2 + (1-x)*(V)

# Dove fitness
def get_fd(V,C,x):
    return x*0 + (1-x)*(V/2)


def plot_single_run(data, V, C, id):
    equil = V/C
    plt.title(id)
    plt.ylabel("Fraction of Hawks")
    plt.xlabel("Time")
    plt.plot(data,label="Empirical")
    plt.axhline(y=equil, color='r', linestyle='--',label=f"Equilibrium ({round(equil,3)})")
    plt.legend(loc="upper right")

    if equil < 1:
        plt.ylim(0,1)
    plt.show()

def plot_multiple_runs(data, V, C):

    equil = V/C

    for log in data:
        plt.plot(data[log])

    plt.axhline(y=equil, color='r', linestyle='--',label=f"Equilibrium ({round(equil,3)})")


    plt.title(f"V={V}, C={C}")
    plt.ylabel("Fraction of Hawks")
    plt.xlabel("Time")
    #plt.legend(loc="upper right")

    if equil < 1:
        plt.ylim(0,1)
    plt.show()


def run_sim(V, C, x_i):
    run_id = f"V={V}, C={C}, x0={x_i}"
    
    dt = 0.1
    T = 100

    x = x_i

    log = []

    for t in np.arange(0, T, dt):

        fh = get_fh(V,C,x)
        fd = get_fd(V,C,x)

        f_avg = x*fh + (1-x)*fd

        dx = x*(fh - f_avg)

        x = x + dx*dt

        log.append(x)


    return log, run_id



def vary_initial_x(V,C,inc=0.01,upto=1):
    data = {}
    for x_i in np.arange(0, upto, inc):
        results, id = run_sim(V,C,x_i)
        data[id] = results

    plot_multiple_runs(data, V, C)


    



# results, id =run_sim(V,C,INITIAL_HAWK_FRACTION)
# plot_single_run(results, V, C, id)

vary_initial_x(V,C)