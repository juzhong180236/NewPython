import numpy as np
from threading import Thread


# a = [[1, 2, 5], [3, 4, 6]]
# print(type(1))
# b = [1, 2, 3, 4, 4, 5]
# print(list(map(lambda x: -x[1] if x[0] % 3 == 0 else x[1], enumerate(b))))

def fun(x1, y1, x2, y2, x):
    temp = (y2 - y1) / (x2 - x1)
    y = temp * (x - x1) + y1
    return y


# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073))
# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073 * 2))
# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073 * 2 + 0.074))
#
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073))
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073 * 2))
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073 * 2 + 0.074))

print(np.arctan(80 / 280) * 180 / np.pi)
