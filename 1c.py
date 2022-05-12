import scipy
from scipy import optimize
import math

import random
import matplotlib.pyplot as plt


# got n_list by running it through 1b
n_list = [11,   6,    4,    4]
p_list = [0.01, 0.04, 0.07, 0.1]

y_vals = []
for i, p in enumerate(p_list):
    total_tests_list = []

    n = n_list[i]
    # simulate it 1000s for each p
    for y in range(1000):
        population = []
        # create population
        for x in range(10000):
            population.append(random.random() <= p)

        # count_a = population.count(True)
        # print(count_a)

        # the first time: number of groups to test
        total_tests = 10000/n
        # actual simulation
        for i in range(0, 10000, n):
            group = population[:n+1]
            # if any in the group are positive, add the total group size to test
            if any(group):
                total_tests += n

            population = population[n:]

        print(len(total_tests_list))
        total_tests_list.append(total_tests)

    avg_total_test = sum(total_tests_list) / len(total_tests_list)
    y_vals.append(avg_total_test)

plt.plot(p_list, y_vals)
plt.show()
