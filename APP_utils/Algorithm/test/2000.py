import numpy as np
import matplotlib.pyplot as plt

# Sample from the Gaussian process
num_of_points = 50  # Number of points in each function
num_of_functions = 5  # Number of functions to sample
# Independent variable samples
X = np.linspace(-4, 4, num_of_points)


def mean(x):
    return np.zeros(x.shape)


def cov(x):
    def squared_exponential_kernel(x1, x2):
        if x1.ndim == 1 and x2.ndim == 1:
            x1 = x1.reshape(-1, 1)
            x2 = x2.reshape(-1, 1)
        from scipy.spatial.distance import cdist
        dx = cdist(x1, x2)
        return np.exp(-(dx ** 2) / 2)

    return squared_exponential_kernel(x, x)


ys = np.random.multivariate_normal(
    mean=mean(X), cov=cov(X),
    size=num_of_functions)
plt.figure(figsize=(10, 5))
for i in range(num_of_functions):
    plt.plot(X, ys[i])
plt.show()
