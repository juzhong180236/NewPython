from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt


def parabola(x, a, b):
    """Return y = a + b*x**2."""
    return a + b * x ** 2


# Define the model inputs
problem = {
    'num_vars': 2,
    'names': ['a', 'b'],
    'bounds': [[0, 1]] * 2
}
# sample N理想情况下是2的幂<= 'skip_values'， 有个skip_values不设置的话默认为16,默认值:2的幂>= N或16，更大的那个
param_values = saltelli.sample(problem, 16)  # 第二个参数需要是2**n
print(param_values)
# N=8，8*(2+2) np.linspace(0, 1, 33)
# N=16，16*(2+2) np.linspace(0, 1, 65)
print(np.linspace(0, 1, 65))
