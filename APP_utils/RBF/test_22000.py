import numpy as np
import time
import matplotlib.pyplot as plt

# def RBF_result(x, c, s):
#     return np.exp(-(x - c) ** 2 / (2 * s ** 2))
#
#
# start = time.perf_counter()
# X = np.arange(0, 22000)
# list_F = []
# for i in range(22000):
#     Gaussian_result = np.array(RBF_result(i, 0, 2))
#     F = Gaussian_result.dot(0.3) + 0.2
#     list_F.append(F)
# plt.plot(X, list_F, color='#0000ff', marker='+', linestyle='-', label='predict')
# plt.tight_layout()
# plt.show()
# elapsed = (time.perf_counter() - start)
# print("Time used:", elapsed)
list_wb_z = np.array([3, 1])
# np.concatenate((list_wb_z, [2, 5]))
# print(np.concatenate((list_wb_z, np.array([[2, 5], [1, 2]]))))
print(np.concatenate((list_wb_z, (2, 5))))
