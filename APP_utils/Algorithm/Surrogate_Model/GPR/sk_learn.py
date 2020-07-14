from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF
import matplotlib.pyplot as plt
import numpy as np


def y(x, noise_sigma=0.0):
    x = np.asarray(x)
    # y = (6 * x - 2) ** 2 * np.sin(12 * x - 4)
    y = np.sin(x) + np.cos(x) + np.random.normal(0, noise_sigma, size=x.shape)
    return y.tolist()


real_x = np.linspace(0, 10, 200)
real_y = y(real_x)
train_X = np.array([0, 3, 4, 7,10]).reshape(-1, 1)
train_y = y(train_X, noise_sigma=0.1)
test_X = np.arange(0, 10, 0.1).reshape(-1, 1)
# fit GPR
kernel = ConstantKernel(constant_value=0.2, constant_value_bounds=(1e-4, 1e4)) * RBF(length_scale=0.5,
                                                                                     length_scale_bounds=(1e-4, 1e4))
# 当参数 normalize_y=False 时，先验的均值 通常假定为常数或者零;
# 当 normalize_y=True 时，先验均值通常为训练数 据的均值
# 先验的方差通过传递 内核(kernel) 对象来指定
# 通过设置内核的超参初始值来进行第一次优化的运行。后续的运行 过程中超参值都是从合理范围值中随机选取的。
# 如果需要保持初始化超参值， 那么需要把优化器设置为 None
# 目标变量中的噪声级别通过参数 alpha 来传递并指定
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=2)
gpr.fit(train_X, train_y)
mu, cov = gpr.predict(test_X, return_cov=True)
test_y = mu.ravel()
uncertainty = 1.96 * np.sqrt(np.diag(cov))

# plotting
plt.figure()
plt.title("l=%.1f sigma_f=%.1f" % (gpr.kernel_.k2.length_scale, gpr.kernel_.k1.constant_value))
plt.fill_between(test_X.ravel(), test_y + uncertainty, test_y - uncertainty, alpha=0.1)
plt.plot(test_X, test_y, label="predict")
plt.plot(real_x, real_y, label="real")
plt.scatter(train_X, train_y, label="train", c="red", marker="x")
plt.legend()
plt.show()
