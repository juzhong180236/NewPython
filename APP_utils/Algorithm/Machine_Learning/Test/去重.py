import numpy as np

a = np.array([1, 2, 3, 4, 4, 5, 6, 6, 6, 6, 8, 89])
b = np.unique(a)
print(b)
a1 = a.reshape(-1, 2)
print(a1)
# b1 = np.unique(a1)
# print(b1)

# 二维数组去重可以先转换为虚数
x = a1[:, 0] + a1[:, 1] * 1j
print(x)

print(a1[np.unique(x, return_index=True)[1]])

print(list(set([tuple(i) for i in a1])))


