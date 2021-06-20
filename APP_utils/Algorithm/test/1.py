import numpy as np
import pandas as pd

# # small R^2
# def small_r2(data_high, data_low):
#     numerator = np.sum((data_high - np.average(data_high)) * (data_low - np.average(data_low)))
#     denominator = np.sqrt(np.sum((data_high - np.average(data_high)) ** 2)) * np.sqrt(
#         np.sum((data_low - np.average(data_low)) ** 2))
#     return numerator / denominator
#
#
# print(np.sqrt(3))
# print(np.sqrt(9))

# x = np.array([1, 2, 3, 2, 3, 4]).reshape(-1, 3)
# print(x)
# [x1, x2] = x.shape
# print(x1, x2)
# dist = np.arange(1, 10).reshape(3, 3)
# dist1 = np.arange(10, 19).reshape(3, 3)
# print(dist)
# print(dist1)
# print(dist1 * dist)
# a = np.array([3, 4, 5]).reshape(-1, 1)
# b = np.array([6, 8, 7]).reshape(-1, 1)
# c = np.array([1, 2, 3]).reshape(-1, 1)
#
# print(np.array([a, b]))
# print(np.hstack([a, b, c]))
# print(np.concatenate((a, b, c), axis=1))
mm = np.array([[469.87, 31.9, 214.2, 246.1],
               [31.9, 3., 14., 17., ],
               [214.2, 14., 98., 112., ],
               [246.1, 17., 112., 129., ]])
print(np.linalg.det(mm))
