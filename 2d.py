import numpy as np

# For p values in [.01, .04, .07, .1] find the optimal n
p_values = [.01, .04, .07, .1]

# Possible n-values that could optimize n_star
# They must be powers of 2 
n_range = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

# This function finds the optimal n that maximizes
# n/b for each p value in our range
def optimal_n(p):
    # start by saying the first n in n_range is most efficient
    curr_most_eff_n = 2
    n_star_eff = 2/b(2,p)
    # if any n-value in the range maximizes n_star 
    # more than the previous ones, update the most
    # efficient n and maximum n_star
    for n in n_range:
        n_star = n/b(n,p)
        if n_star > n_star_eff:
            n_star_eff = n_star
            curr_most_eff_n = n
    return curr_most_eff_n

# This function computes the expetced value of Bn in 
# terms of the expected value of Cn
def b(n,p):
    if (n == 2):
        return -2*p*p + 4*p +1
    return (1-p)**n + (1-((1-p)**n))*(1+c(n,p))

# This function computes the expetced value of Cn in 
# terms of the expected value of Cn and Bn
def c(n,p):
    if (n == 2):
        return 2
    return (((1-p)**n)*(1 + c(n/2,p))) + ((1-((1-p)**n))*(1 + c(n/2,p) + b(n/2,p)))


n_optimal = [optimal_n(p) for p in p_values]
print(n_optimal)