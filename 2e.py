import matplotlib.pyplot as plt

# Steps for Finding the Expected Number of Tests Under the Binary Splitting Strategy
# For a specific p-value, divide the population by the optimal group size
# (Ex : 10, 000 / 64 = 156  with remainder 16)
# Then find the expected number of tests by looping ex: 156 times and adding
# b(n,p) and then one time add the n = remainder number of expected tests

# Expected value of Bn
def b(n,p):
    if (n == 2):
        return -2*p*p + 4*p +1
    return (1-p)**n + (1-((1-p)**n))*(1+c(n,p))

# Expected value of Cn
def c(n,p):
    if (n == 2):
        return 2
    return (((1-p)**n)*(1 + c(n/2,p))) + ((1-((1-p)**n))*(1 + c(n/2,p) + b(n/2,p)))

# This function calculates the expected number of tests
# for a population of N = 10,000, an infection rate of p
# and an optimal group size n
def num_test_b (n, p):
    remainder = 10000%n
    num_optimal_groups = int((10000-remainder)/n)
    num_tests = 0

    for i in range(num_optimal_groups):
        num_tests += b(n,p)

    if (remainder >= 2):
        num_tests += b(remainder,p)

    return num_tests

print(num_test_b(64, .01))
print(num_test_b(16, .04))
print(num_test_b(8, .07))
print(num_test_b(8, .1))


# Now with the Dorfman Strategy
# Calculate the expected number of tests needed for groups of size n
# with probability p of infection, then loop through just as above

# Expected value of Dn 
def d(n,p):
    if (n == 1):
        return 1
    return n - n*((1-p)**n) + 1

# Same function as num_test except using Dorfman testing
def num_test_d (n, p):
    remainder = 10000%n
    num_optimal_groups = int((10000-remainder)/n)
    num_tests = 0

    for i in range(num_optimal_groups):
        num_tests += d(n,p)

    if (remainder >= 1):
        num_tests += d(remainder,p)

    return num_tests


print(num_test_d(11, .01))
print(num_test_d(6, .04))
print(num_test_d(4, .07))
print(num_test_d(4, .1))


x_values = [0.01, 0.04, 0.07, 0.1]
y_values = [num_test_b(64, .01)/num_test_d(11, .01), num_test_b(16, .04)/num_test_d(6, .04),
            num_test_b(8, .07)/num_test_d(4, .07), num_test_b(8, .1)/num_test_d(4, .1)]
plt.plot(x_values, y_values)
plt.xlabel("p-value")
plt.ylabel("E[Dn] / E[Bn] using optimal n")
plt.title("Ratio of Binary to Dorfman Expected Tests")
plt.show()