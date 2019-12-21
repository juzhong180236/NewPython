import numpy as np


def multiquadric(x, c, s):
    if c.ndim != 1:
        return np.sqrt(np.sum((x - c) ** 2, axis=-1) + s ** 2)  # mq多维正确公式
    else:
        return np.sqrt((x - c) ** 2 + s ** 2)


def linear_abs(x, c):
    if c.ndim != 1:
        return np.sum(np.abs(x - c), axis=-1)
    else:
        return np.abs(x - c)


a = np.array([[1, 2, 3], [3, 4, 5]])
for i in range(a.shape[0]):
    print(linear_abs(a[i], a))
print('fas')
aa = np.array([1, 2, 3, 3, 4, 5])
for i in range(aa.shape[0]):
    print(linear_abs(aa[i], aa))

a = np.array([[1, 2, 3], [3, 4, 5]])
matrix = []
for i in range(a.shape[0]):
    print(multiquadric(a[i], a, 2))
    matrix.append(multiquadric(a[i], a, 2))
print(np.linalg.pinv(matrix))

print('fas')
aa = np.array([1, 2, 3, 3, 4, 5])
for i in range(aa.shape[0]):
    print(multiquadric(aa[i], aa, 2))
