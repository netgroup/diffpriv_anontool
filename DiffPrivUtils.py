import Const
import math
import numpy as np

from decimal import Decimal


# This class provides differential privacy by adding Laplace noise.
class Laplace:

    def __init__(self, sensitivity=1.0, epsilon=math.log(3)):
        self.sensitivity = sensitivity
        self.epsilon = epsilon
        self.diversity = sensitivity / epsilon

    # Generates samples from the Laplace Distribution according to the Ratio of Uniforms method outlined in Section 4.7
    # Devroye, Luc. "Non-Uniform Random Variate Generation"(1987): 195. Cleaner and more accurate than the typical
    # Inverse CDF method under fixed precision arithmetic.
    def sample(self, scale):
        u1 = np.random.uniform()
        u2 = np.random.uniform()
        value = math.log(u1 / u2) * (scale * self.diversity)
        if value == -float(Const.INFINITY) or value == float(Const.INFINITY):
            return 0.0
        return value


kClampFactor = 2 ** 39


# Set lower bound to the bigger between infinity float representation and -kClampFactor
def lower_bound():
    return max(-float(Const.INFINITY), -kClampFactor)


# Set upper bound to the smaller between infinity float representation and -kClampFactor
def upper_bound():
    return min(float(Const.INFINITY), kClampFactor)


# Bind value in the range [lower, upper]
def clamp(lower, upper, value):
    if value > upper:
        return upper
    if value < lower:
        return lower
    return value


# Compute the power of 2 and nearest integer to log2(n)
def next_power_of_two(n):
    return 2**math.ceil(math.log(n, 2))


# Adds differentially private noise to a provided value. The privacy_budget is multiplied with epsilon for this
# particular result. Privacy budget should be in (0, 1], and is a way to divide an epsilon between multiple values. For
# instance, if a user wanted to add noise to two different values with a given epsilon then they could add noise to each
# value with a privacy budget of 0.5 (or 0.4 and 0.6, etc).
def add_noise(result, budget, sensitivity, epsilon):
    laplace = Laplace(sensitivity=sensitivity, epsilon=epsilon)
    noise = laplace.sample(1.0/budget)
    noised_result = clamp(lower_bound(), upper_bound(), result) + noise
    nearest_power = next_power_of_two(laplace.diversity / budget)
    remainder = 0.0 if nearest_power is 0.0 else float(Decimal(noised_result) % Decimal(nearest_power))
    rounded_result = noised_result - remainder
    return clamp(lower_bound(), upper_bound(), rounded_result)
