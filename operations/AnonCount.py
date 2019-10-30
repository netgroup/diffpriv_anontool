import os

from subprocess import check_output

import FuncUtils as fu
from operations.Laplace import Laplace

from decimal import Decimal


# Adds differentially private noise to a provided value. The privacy_budget is multiplied with epsilon for this
# particular result. Privacy budget should be in (0, 1], and is a way to divide an epsilon between multiple values. For
# instance, if a user wanted to add noise to two different values with a given epsilon then they could add noise to each
# value with a privacy budget of 0.5 (or 0.4 and 0.6, etc).
# def add_noise(result, budget, sensitivity, epsilon):
#     laplace = Laplace(sensitivity=sensitivity, epsilon=epsilon)
#     noise = laplace.sample(1.0/budget)
#     noised_result = fu.clamp(fu.lower_bound(), fu.upper_bound(), result) + noise
#     nearest_power = fu.next_power_of_two(laplace.diversity / budget)
#     remainder = 0.0 if nearest_power is 0.0 else float(Decimal(noised_result) % Decimal(nearest_power))
#     rounded_result = noised_result - remainder
#     return fu.clamp(fu.lower_bound(), fu.upper_bound(), rounded_result)


# Compute an anonymous count of data
def compute(epsilon, budget):
    os.chdir('/diffpriv/differential-privacy-master/')
    return check_output(['/root/bin/bazel run differential_privacy/operations:anon_count -- %s %s'
                         % (epsilon, budget)], shell=True)

# def compute(data, epsilon, budget):
#     noised_result = int(round(add_noise(result=data.size, budget=budget, sensitivity=1.0, epsilon=epsilon)))
#     fu.log(fu.get_current_time() + 'Executed anon_count with epsilon = ' + str(epsilon) + ' and budget = ' + str(budget)
#            + ', resulting in anon_count = ' + str(max(noised_result, 0)) + ' where real count = ' + str(data.size) +
#            '\n')
#     return max(noised_result, 0)
