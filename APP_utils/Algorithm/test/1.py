import numpy as np
from threading import Thread
from APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS import PRS


# from APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS import PRS
def spherical_variogram_model(m, d):
    """Spherical model, m is [psill, range, nugget]"""
    psill = float(m[0])  # c1
    range_ = float(m[1])  # c2
    nugget = float(m[2])  # c0
    return np.piecewise(
        d,
        [d <= range_, d > range_],
        [
            lambda x: psill * ((3.0 * x) / (2.0 * range_) - (x ** 3.0) / (2.0 * range_ ** 3.0)) + nugget,
            psill + nugget,
        ],
    )


def a(m, d):
    c1 = float(m[0])  # c1
    c2 = float(m[1])  # c2
    c0 = float(m[2])  # c0
    return np.piecewise(
        d,
        [d <= c2, d > c2],
        [
            lambda x: c1 * ((3.0 * x) / (2.0 * c2) - (x ** 3.0) / (2.0 * c2 ** 3.0)) + c0,
            c1 + c0,
        ],
    )


def spherical(_d, _theta):
    m, n = _d.shape
    td = min(abs(_d) * np.tile(_theta, m).any(), [1])
    print(td)
    return list(map(lambda _x: 1 - (1.5 * _x / _theta - (_x ** 3.0) / (2.0 * _theta ** 3.0)), _d))


# d = np.array([1, 2, 3]).reshape(-1, 3)
# theta = np.array([2, 3, 4])
# spherical(d, theta)

print(min([1, 3, 4], [1, 1, 1]))


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

# print(np.arctan(80 / 280) * 180 / np.pi)
# X_pre = np.array([3, 2])
# list_temp = []
# for i in range(X_pre.shape[0]):
#     _list_temp = []
#     for j in range(3 + 1):
#         _list_temp.append(X_pre[i] ** j)
#     list_temp.append(np.array(_list_temp))
# print(list_temp)
# x_train = np.array([[3, 2, 5], [2, 3, 4], [4, 5, 6]])
# y_train = np.array([4, 5, 5])
# p = PRS()
# print(p.calc_gram_matrix(x_train))
# p.fit(y_train)

# x = np.arange(0, 10)
# print(x)
# xx = np.piecewise(x, [x < 4, x >= 6], [-1, 1])
# print(xx)
# print(spherical_variogram_model(np.array([3, 4, 5]), 6))
