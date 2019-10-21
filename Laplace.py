import Const
import math
import numpy as np


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
