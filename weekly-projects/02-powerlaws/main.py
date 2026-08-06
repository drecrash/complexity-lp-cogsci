import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import pareto

N = 1000
POWER = 0.5

alpha = 5

xmin = 10

generator = np.random.default_rng()
distrib = pareto.rvs(b=alpha-1,scale=xmin,size=N)

def compute_ml_pareto(vals):
    n = len(vals)
    logged = np.log(vals)
    summation = sum(logged)

    a = pow((summation/n)-np.log(xmin),-1)+1

    return a

def fit_func(exponent, x):
    return np.pow(x, -exponent)*(exponent-1)*pow(xmin, exponent-1)

slope = compute_ml_pareto(distrib)
plt.hist(distrib, density=True)
fit_x = np.linspace(min(distrib),max(distrib),N)
plt.plot(fit_x, fit_func(slope, fit_x),label=f"approx λ={round(slope,5)}\nreal λ={alpha}")
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()