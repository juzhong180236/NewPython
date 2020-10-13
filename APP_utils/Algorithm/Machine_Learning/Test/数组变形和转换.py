import numpy as np

a = np.arange(27).reshape((3, 3, 3))
# print(np.dsplit(a, 3))

a1 = np.arange(4).reshape(2, 2)
b1 = np.arange(4, 8).reshape(2, 2)

# print(np.r_[a1, b1])
# print(np.hstack([a1, b1]))
# print(np.hsplit(a1, 2))
x = [i for i in range(10)]
# print(x)

a2 = np.arange(0, 20, 10).reshape(-1, 1)
b2 = np.arange(0, 3)
# print(a2.ndim)
print(a2)
print(b2)

a3 = np.arange(0, 27).reshape((3, 3, 3))
b3 = np.arange(0, 3)
# print(a3 + b3)
