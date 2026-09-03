import numpy as np
from scipy.fft import dctn
import pywt
import pulp

from pulp import *

from PIL import Image

import matplotlib.pyplot as plt

DIMENSION = 16*16
PATCH_SIZE = int(math.sqrt(DIMENSION))
perturbation = 0

def get_image_vector(path):
    img = Image.open(path).convert("L")
    img_array = np.array(img, dtype=float)
    

    for row in range(0, DIMENSION*2, PATCH_SIZE):
        for col in range(0, DIMENSION*2, PATCH_SIZE):
            patch = img_array[row:row+PATCH_SIZE, col:col+PATCH_SIZE].flatten()
            if patch.std() > 20:
                segment = img_array[row:row+PATCH_SIZE, col:col+PATCH_SIZE].flatten()
                return segment

    return None

def wavelet_basis(n, wavelet='haar'):
    B = np.zeros((n, n))

    for i in range(n):

        s = np.zeros(n)
        s[i] = 1
        coefficients = pywt.wavedec(s, wavelet, level=4)
        B[:, i] = np.concatenate([c for c in coefficients])

    return B

def visualize_solution(a_values,basis):
    a_values = np.array(a_values)
    
    reconstruction = basis @ a_values

    arr = reconstruction.reshape(PATCH_SIZE, PATCH_SIZE)
    plt.imshow(arr, cmap='viridis')

    plt.show()

basis = dctn(np.eye(DIMENSION)).T
#basis = wavelet_basis(DIMENSION)



a = list(range(DIMENSION))

prob = LpProblem("pursuit", LpMinimize)

x = get_image_vector("test2.png")

x = x - x.mean()

x = x / x.std()


t_var = pulp.LpVariable.dicts(f"t", a,lowBound=0)
a_var = pulp.LpVariable.dicts(f"a", a)

prob += lpSum(list(t_var.values()))

for i in a:
    prob+= t_var[i] >= a_var[i]*-1
    prob += t_var[i] >= a_var[i]


for m in range(DIMENSION):
    #prob += lpSum([basis[m,i]*a_var[m] for i in a]) == x[m]

    prob += lpSum([basis[m,i]*a_var[i] for i in a]) <= x[m] + perturbation
    prob += lpSum([basis[m,i]*a_var[i] for i in a]) >= x[m] - perturbation



status = prob.solve()

print(LpStatus[status])

for i, a in a_var.items():
    if a.value() !=0:
        print(f"{i}: {a.value()}")

is_zero = len([i for i in a_var.values() if i.value() == 0])

print(f"{is_zero} coefficients are zero")

visualize_solution([i.value() for i in a_var.values()],basis)