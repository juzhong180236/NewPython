import numpy as np


def multiquadric(x, c, s):
    if c.ndim != 1:
        print(np.sqrt(np.sum((x - c) ** 2, axis=-1)) + s ** 2)
        return np.sqrt(np.sqrt(np.sum((x - c) ** 2, axis=-1)) + s ** 2)
    else:
        return np.sqrt((x - c) ** 2 + s ** 2)


a = np.array([[1, 2, 3], [3, 4, 5]])
for i in range(a.shape[0]):
    print(multiquadric(a[i], a, 3))
