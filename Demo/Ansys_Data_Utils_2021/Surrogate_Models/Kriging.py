import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D


class Kriging(object):
    def __init__(self, theta=0.1, p=2):
        self.X = None
        self.Y = None
        self.theta = theta
        self.beta = None
        self.sigma2 = None
        self.inverse_matrix = None
        self.F = None

    def gaussian_kernel(self, x1, x2):
        list_result = []
        if x1.shape[-1] != 1:
            for x1_ele in x1:
                list_result.append(np.exp(np.sum(-self.theta * (x1_ele - x2) ** 2, axis=-1)).ravel())
        else:
            for x1_ele in x1:
                list_result.append(np.exp(-self.theta * (x1_ele - x2) ** 2).ravel())
        return np.asarray(list_result)

    def negative_log_likelihood_loss(self, _theta):
        self.theta = _theta
        correlation_matrix = self.gaussian_kernel(self.X, self.X) + 1e-8 * np.eye(len(self.X))
        inverse_matrix = np.linalg.inv(correlation_matrix)
        # 均值
        self.beta = self.F.T.dot(inverse_matrix).dot(self.Y) / (self.F.T.dot(inverse_matrix).dot(self.F))
        # print(self.beta)
        # 方差
        self.sigma2 = ((self.Y - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(self.Y - self.F.dot(self.beta))) / \
                      self.F.shape[0]
        # print(self.sigma2)
        R = np.linalg.det(correlation_matrix)
        return np.log(self.sigma2) * (self.F.shape[0] / 2) + 1 / 2 * np.log(R)

    def train(self, x, y):
        self.X = np.asarray(x)
        self.Y = np.asarray(y).reshape(-1, 1)
        self.F = np.ones(x.shape[0]).reshape(-1, 1)
        # 拟牛顿法：BFGS
        # 未知方法
        res = minimize(self.negative_log_likelihood_loss, self.theta,
                       bounds=[(0.1, 10)],
                       method='L-BFGS-B')
        # 牛顿-共轭梯度法：Newton-CG
        # res = minimize(self.negative_log_likelihood_loss, self.parameter, method='nelder-mead')
        # 单纯形法：Nelder-Mead
        # res = minimize(self.fitness, self.parameters, method='BFGS')
        self.theta = res.x
        correlation_matrix = self.gaussian_kernel(self.X, self.X)

        self.inverse_matrix = np.linalg.inv(correlation_matrix)
        self.beta = self.F.T.dot(self.inverse_matrix).dot(self.Y) / (self.F.T.dot(self.inverse_matrix).dot(self.F))

    def predict(self, x_pre):
        # 相关向量
        vector = self.gaussian_kernel(self.X, np.asarray(x_pre))
        # 预测值
        y_pre = self.beta + vector.T.dot(self.inverse_matrix).dot(
            self.Y - self.F.dot(self.beta))
        return y_pre


if __name__ == "__main__":
    def curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    # def curve(x):
    #     return np.sum((6 * x - 2) ** 2 * np.sin(12 * x - 4), axis=-1)

    parameter = np.array([0.3])
    x_real = np.linspace(0, 1).reshape(-1, 1)
    y_real = curve(x_real).reshape(-1, 1)
    # x_train = np.array([0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]).reshape(-1, 1)
    x_train = np.array([0, 0.4, 0.6, 1]).reshape(-1, 1)
    y_train = curve(x_train)
    # y_train = np.asarray([1, 1, 1, 1])
    # print(y_train)

    kriging = Kriging()
    kriging.train(x_train, y_train)

    x_pred = np.linspace(0, 1).reshape(-1, 1)
    y_pred = kriging.predict(x_pred)


    # R^2
    def r2(data_real, data_predict):
        RSS = np.sum((data_predict - data_real) ** 2)
        TSS = np.sum((data_real - np.average(data_real)) ** 2)
        return 1 - RSS / TSS


    # plt.plot(range(x_pred.shape[0]), y_pred, color='#00ffff', label='predicted value', linestyle='-')
    # plt.plot(range(x_real.shape[0]), y_real, color='#ff0000', label='real value', linestyle='-')
    # plt.scatter(range(x_train.shape[0]), y_train, color='#0000ff', label='train set', marker='s')

    # print(y_real)
    # print(y_pred)
    # print(r2(y_real, y_pred))
    plt.plot(x_pred, y_pred, color='#00ffff', label='predicted value', linestyle='-')
    plt.plot(x_real, y_real, color='#ff0000', label='real value', linestyle='-')
    plt.scatter(x_train, y_train, color='#0000ff', label='train set', marker='s')
    plt.legend()
    plt.show()
