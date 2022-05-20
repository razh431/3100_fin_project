import scipy
from scipy import optimize
import math
import random
import matplotlib.pyplot as plt

n_list = [11,   6,    4,    4]
p_list = [0.01, 0.04, 0.07, 0.1]

y_vals = []
for i, p in enumerate(p_list):
    ratio_list = []

    n = n_list[i]
    # simulate it 1000s for each p
    for y in range(1000):
        population = []
        # create population
        for x in range(10000):
            population.append(random.random() <= p)

        # Total tests: Dorfman
        total_tests_1 = 10000/n

        # Dorfman Testing
        for i in range(0, 10000, n):
            group = population[:n+1]
            # if any in the group are positive, add the total group size to test
            if any(group):
                total_tests_1 += n

            population = population[n:]  # iterate through population in blocks

        ratio_list.append(total_tests_1/10000)

    avg_total_test = sum(ratio_list) / len(ratio_list)
    y_vals.append(avg_total_test)

plt.xlabel("p")
plt.ylabel("Number of Dorfman Tests/ Number of Individual Tests")
plt.title("Ratio of Dorfman tests to Individual Tests vs. p")
plt.plot(p_list, y_vals)
plt.show()
