import numpy as np

a = np.arange(0, 100).reshape(2, 50)
print(a[1, :])

# 维度是由外及内
# a = np.arange(0, 60, 10).reshape(-1, 1) + np.arange(8)
# F1 = np.array([1]).reshape(-1, 1)
# print(F1)
# y = np.random.normal(0, 0.1, size=5)
# y2 = np.random.normal(0, 0.1, size=5)
#
# Y = np.vstack([y, y2])
#
# print(Y[:, 1])
# print(Y)

# print(np.arange(0, 60, 10).reshape(-1, 1))
# print(np.arange(6))
# print(a)
# print(np.arange(0, 60, 10).reshape(-1, 1))
# print(a.itemsize)
# b = np.array([[1, 2], [3, 4], [5, 6]])
# print(b[[0, 1], [0, 1]])
# aa = np.array([1, 2, 3, 4, 5])
# print(np.append(aa, 4))
# print(aa)
# b = np.arange(1, 13).reshape(3, 4)
# c = b.reshape(4, 3)
# d = np.arange(1, 13).reshape(3, 4)
# print(b)
# print(c)
# c[0][1] = 20
# print(b)
# print(c)
# print(d)
# print(type(b))
# print(b.dtype)
# m = b.astype(np.float)
# print(m)
# m[0][0] = 3
# print(m)
# print(b)
# # np.set_printoptions(linewidth=200, suppress=True)
# # 10^1到10^2之间取10个数
# np.logspace(1, 2, 10, endpoint=True)
# # 从2^1到2^10之间取10个数
# np.logspace(1, 2, 10, endpoint=True, base=2)
# s = "mytestfromstring"
# # print(np.fromstring(s, dtype=np.float))
# #
# # print(s[::-1])
# # 切片[0][3] [1][4] [2][5]
# # print(a[[0, 1, 2], [3, 4, 5]])
# # print(a[4, [3, 4, 5]])
# # print(a[4:, [3, 4, 5]])
# i = np.array([True, False, True, True, False, False])
# print(a[i])
# print(a[i, 3])
