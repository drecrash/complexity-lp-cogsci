import random
import numpy as np
import matplotlib.pyplot as plt


def plot_distrib(results,title=""):
    plt.hist(results,density=True)
    plt.title(title)
    plt.show()


def uniform_distrib(iterations, samples,normalize=False):
    results = []

    for i in range(iterations):
        sample_data = np.random.uniform(0,1,samples)
        sum_ = np.sum(sample_data)
        prod = 1

        if (normalize):
            for d in sample_data:
                prod *= d/sum_
        else:
            prod = np.prod(sample_data)

        results.append(prod)

    return results

plot_distrib(uniform_distrib(100000, 10, True),title="Normalization On")
plot_distrib(uniform_distrib(100000, 10, False), title="Normalization Off")

