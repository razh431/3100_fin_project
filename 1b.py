import scipy
from scipy import optimize
import math

import matplotlib.pyplot as plt

p = 0.001


def n_star(x, p):
    return x/((1-p) ** x + (x+1)*(1-(1-p) ** x))


def rounded_n(exact_val, p):
    max_int = math.floor(exact_val)
    min_int = math.ceil(exact_val)
    return max_int if n_star(max_int, p) > n_star(min_int, p) else min_int


p_vals = []
n_stars = []
p_list = [0.01, 0.04, 0.07, 0.1]

# for part 1c
p_c = []
while p < 0.4:
    exact_val = scipy.optimize.fmin(lambda x: -n_star(x, p), 0)

    if n_star(exact_val, p) < 1:
        n_star_val = 1
    else:
        n_star_val = rounded_n(exact_val, p)
    n_stars.append(n_star_val)
    p_vals.append(p)
    p += 0.001

print(p_c)
plt.plot(p_vals, n_stars)
plt.show()
