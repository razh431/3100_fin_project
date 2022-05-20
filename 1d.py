from cgi import test
from distutils.command import config
import math
import random
import matplotlib.pyplot as plt


pt_d_n_stars = [23, 19, 16, 15, 13, 12, 12,
                11, 11, 10, 10, 9, 9, 9, 8, 8, 8, 8, 8]


def testing(p, test):
    if test > 500:
        return "exceeded"
    return random.random() <= p


def test_small_group(n, p):
    # each big group test, has to keep the group for the next day
    group = []
    next_day_testing = []  # if positive, this list should be the group

    # create group
    for i in range(n):
        group.append(random.random() <= p)

    if any(group):  # if anyone is positive, add it to the next day
        # cant_work_day = n  # number of people who can't work until day day
        next_day_testing = group[:]

    return next_day_testing


def dorfman():
    x_vals = []

    y_vals = []
    for k in range(19):
        p = 0.002 + 0.001*k  # get the p value associated the n
        n = pt_d_n_stars[k]
        x_vals.append(p)

        confine_cost = 0  # over 10 iterations, divide by 10 at end
        for ave in range(10):
            infected = []
            healthy = []
            test_per_day = 0

            # create population
            for x in range(10000):
                infected.append(0) if testing(
                    p, test_per_day) else healthy.append(0)

            group_pos_list = []
            for days in range(90):
                test_per_day = 0
                cant_work = 0

                # test people that group tested pos the day before:
                for i in range(len(group_pos_list)):
                    ind_group = group_pos_list[i]
                    infected_num = sum(map(lambda x: x == True, ind_group))
                    for x in range(infected_num):
                        infected.append(0)

                    healthy_num = len(ind_group) - infected_num
                    for x in range(healthy_num):
                        healthy.append(0)  # add them back to healthy

                    test_per_day += len(ind_group)
                    cant_work += len(ind_group)

                    group_pos_list[i] = []

                    if test_per_day + n > 500:
                        break

                group_pos_list = [i for i in group_pos_list if i != []]
                # assign everyone their own testing day
                if 0 <= days < 7:
                    agg_healthy = len(healthy)//7
                    for x in range(0, agg_healthy, n):
                        next_day_testing = test_small_group(
                            n, p)
                        if next_day_testing != []:
                            group_pos_list.append(next_day_testing)
                            cant_work += n
                        else:
                            for x in range(n):
                                healthy.append(0)  # add n 0s to the end

                        if test_per_day < 500:
                            test_per_day += 1
                        else:
                            cant_work += need_testing - 500
                            break

                    healthy[:agg_healthy+1] = [-1] * \
                        agg_healthy  # set the group to tested

                # tests healthy, not first week
                else:
                    # number of people that need to be tested on 7th day, index on 0th
                    need_testing = sum(map(lambda x: x >= 6, healthy))
                    # group testing
                    for x in range(0, need_testing, n):
                        next_day_testing = test_small_group(
                            n, p)
                        if next_day_testing != []:
                            group_pos_list.append(next_day_testing)
                            cant_work += n
                        else:
                            for x in range(n):
                                healthy.append(0)

                        if test_per_day + n < 500:
                            test_per_day += 1
                        else:
                            cant_work += need_testing - 500
                            break

                    healthy[:need_testing+1] = [-1] * \
                        need_testing  # group tested

                # move everyone who's out of quarantine into healthy with testing INDIVIDUALLY
                need_testing_inf = sum(map(lambda x: x > 20, infected))
                for x in range(need_testing_inf):
                    if random.random() <= p:
                        infected.append(0)
                    else:
                        healthy.append(0)
                    infected[x] = -1
                    test_per_day += 1
                    if test_per_day + 1 < 500:
                        cant_work += need_testing_inf - test_per_day
                        break

                if len(group_pos_list) != 0:
                    cant_work += len(group_pos_list*len(group_pos_list[0]))

                confine_cost += (len(infected) + cant_work) * 172

                # remove tested (-1), add 1 day to everyone
                infected = [i + 1 for i in infected if i != -1]
                healthy = [j+1 for j in healthy if j != -1]
                # ran out of tests
                confine_cost += (len(infected) + cant_work) * 172

        y_vals.append(confine_cost/10)

    return x_vals, y_vals


def ind():
    x_vals = []
    y_vals = []
    for k in range(19):
        p = 0.002 + 0.001*k  # get the p value associated the n

        confine_cost = 0  # confined cost over 10 iterations, take average later
        x_vals.append(p)
        for i in range(10):  # average over 10
            test_per_day = 0
            infected = []
            healthy = []

            # create population
            for x in range(10000):
                infected.append(0) if testing(
                    p, test_per_day) else healthy.append(0)

            for days in range(90):
                cant_work = 0
                # assign everyone their own testing day
                if 0 <= days < 7:
                    agg_healthy = len(healthy)//7
                    for x in range(500):
                        infected.append(0) if testing(
                            p, test_per_day) else healthy.append(0)
                        healthy[x] = -1

                    cant_work = agg_healthy - 500  # ran out of tests for individual

                # tests healthy, not first week
                else:
                    # number of people that need to be tested
                    need_testing = sum(map(lambda x: x >= 6, healthy))
                    # group testing
                    for x in range(need_testing):
                        if test_per_day < 500:
                            infected.append(0) if testing(
                                p, test_per_day) else healthy.append(0)
                            healthy[x] = -1
                            test_per_day += 1
                        else:
                            break
                    # ran out of tests
                    cant_work = need_testing - test_per_day

                    # test infected
                    need_testing_infected = sum(
                        map(lambda x: x >= 20, infected))
                    for y in range(need_testing_infected):
                        if test_per_day < 450:
                            infected.append(0) if testing(
                                p, test_per_day) else healthy.append(0)
                            infected[y] = -1
                            test_per_day += 1
                        else:
                            break

                # remove tested, add 1 day to everyone
                infected = [i + 1 for i in infected if i != -1]
                healthy = [j+1 for j in healthy if j != -1]
                test_per_day = 0  # reset the tests to 0, count up to 500

                # print(cant_work)
                confine_cost += (len(infected) + cant_work) * 172
        y_vals.append(confine_cost/10)

    return x_vals, y_vals


# plotting
plt.title("Average Confined Cost (Individual Testing)")
plt.xlabel("P values")
plt.ylabel("Cost ($)")

x_vals, dorf_y_vals = dorfman()
x_valus, ind_y_vals = ind()
plt.plot(x_vals, dorf_y_vals, label="Dorfman")
plt.plot(x_valus, ind_y_vals, label="Individual")
plt.legend()

plt.show()
