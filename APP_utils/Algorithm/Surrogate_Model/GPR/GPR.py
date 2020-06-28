import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class GPR:

    def __init__(self, optimize=False):
        self.is_fit = False
        self.x = None
        self.y = None
        self.params = {"s": 0.5, "sigma": 0.2}
        self.optimize = optimize

        self.Kff = None
        self.Kff_inv = None
        self.X_pre = None
        self.mu = None
        self.cov = None

    def negative_log_likelihood_loss(self, params):
        self.params["s"], self.params["sigma"] = params[0], params[1]
        Kyy = self.kernel(self.x, self.x) + 1e-8 * np.eye(len(self.x))
        return 0.5 * self.y.T.dot(np.linalg.inv(Kyy)).dot(self.y) + 0.5 * np.linalg.slogdet(Kyy)[1] + 0.5 * len(
            self.x) * np.log(2 * np.pi)

    def fit(self, X, Y):
        self.x = np.asarray(X)
        self.y = np.asarray(Y)

        if self.optimize:
            res = minimize(self.negative_log_likelihood_loss, np.asarray([self.params["s"], self.params["sigma"]]),
                           bounds=((1e-4, 1e4), (1e-4, 1e4)),
                           method='L-BFGS-B')
            self.params["s"], self.params["sigma"] = res.x[0], res.x[1]

        self.is_fit = True
        self.Kff = self.kernel(self.x, self.x)  # (N, N)
        self.Kff_inv = np.linalg.inv(self.Kff + 1e-8 * np.eye(len(self.x)))  # (N, N)
        return self.Kff, self.Kff_inv

    def predict(self, X_pre):
        if not self.is_fit:
            print("is_fit is not initialized, please execute fit function first.")
            return
        self.X_pre = np.asarray(X_pre)
        Kyy = self.kernel(self.X_pre, self.X_pre)  # (k, k)
        Kfy = self.kernel(self.x, self.X_pre)  # (N, k)

        self.mu = Kfy.T.dot(self.Kff_inv).dot(self.y)
        self.cov = Kyy - Kfy.T.dot(self.Kff_inv).dot(Kfy)
        return self.mu, self.cov

    def kernel(self, x1, x2):
        dist_matrix = np.sum(x1 ** 2, 1).reshape(-1, 1) + np.sum(x2 ** 2, 1) - 2 * np.dot(x1, x2.T)
        return self.params["sigma"] ** 2 * np.exp(-0.5 / self.params["s"] ** 2 * dist_matrix)


if __name__ == "__main__":
    def y(x, noise_sigma=0.0):
        x = np.asarray(x)
        y = np.cos(x) + np.random.normal(0, noise_sigma, size=x.shape)
        return y.tolist()


    x = np.array([3, 1, 4, 5, 9]).reshape(-1, 1)
    y = y(x, noise_sigma=1e-4)
    test_X = np.arange(0, 10, 0.1).reshape(-1, 1)

    gpr = GPR()  #
    gpr.fit(x, y)  #

    mu, cov = gpr.predict(test_X)

    test_y = mu.ravel()

    uncertainty = 1.96 * np.sqrt(np.diag(cov))

    plt.figure()
    plt.title("s=%.2f sigma=%.2f" % (gpr.params["s"], gpr.params["sigma"]))
    plt.fill_between(test_X.ravel(), test_y + uncertainty, test_y - uncertainty, alpha=0.1)
    plt.plot(test_X, test_y, label="predict")
    plt.scatter(x, y, label="train", c="red", marker="x")
    plt.legend()
    plt.show()
