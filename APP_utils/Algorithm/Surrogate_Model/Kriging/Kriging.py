import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm


class Kriging(object):
    def __init__(self, parameters=None):
        self.X = None
        self.Y = None
        self.parameters = parameters
        self.beta = None
        self.sigma2 = None
        self.inverse_matrix = None
        self.F = None
        self.yc_xe = None
        self.c_matrix = None

    def gaussian(self, para_list, x1, x2):
        if x2.ndim != 1:
            return np.prod(np.exp(-para_list[0] * (x1 - x2) ** 2), axis=-1)
        else:
            return np.exp(-para_list[0] * (x1 - x2) ** 2)

    def corelation(self, func, x, y, para_array):
        list_result = []
        for i in range(x.shape[0]):
            list_result.append(func(para_array, x[i], y).ravel())
        # print(np.array(list_result))
        return np.array(list_result)

    def fitness(self, parameters):
        self.parameters = parameters
        # print(self.parameters)
        matrix = self.corelation(self.gaussian, self.X, self.X, self.parameters) + 1e-8 * np.eye(len(self.X))
        inverse_matrix = np.linalg.inv(matrix)
        # if self.parameters.shape[-1] == 2:
        if self.c_matrix is not None:
            d = self.Y - self.parameters[1] * self.yc_xe
            # d = self.Y
            self.beta = self.F.T.dot(inverse_matrix).dot(d) / (self.F.T.dot(inverse_matrix).dot(self.F))
            # 方差
            self.sigma2 = ((d - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(d - self.F.dot(self.beta))) / \
                          self.F.shape[-1]
            R = np.abs(np.linalg.det(self.c_matrix))
            # R = np.abs(np.linalg.det(matrix))
        else:
            # 均值
            self.beta = self.F.T.dot(inverse_matrix).dot(self.Y) / (self.F.T.dot(inverse_matrix).dot(self.F))
            # 方差
            self.sigma2 = ((self.Y - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(self.Y - self.F.dot(self.beta))) / \
                          self.F.shape[-1]
            R = np.abs(np.linalg.det(matrix))
        # self.sigma2 = np.finfo(np.float64).tiny if self.sigma2 == 0 else self.sigma2
        return np.log(np.abs(self.sigma2)) * (self.F.shape[-1] / 2) + 1 / 2 * np.log(R)

    def fit(self, x, y, yc_xe=None, c_matrix=None):
        if yc_xe is not None:
            self.yc_xe = yc_xe
        if c_matrix is not None:
            self.c_matrix = c_matrix
        self.X = np.asarray(x)
        self.Y = np.asarray(y)
        # print(self.corelation(self.gaussian, self.X, self.X, self.parameters))
        self.F = np.ones(x.shape[-1])
        # 拟牛顿法：BFGS
        # 未知方法
        # res = minimize(self.fitness, self.parameters,
        #                bounds=np.array([1e-4, 1e4] * self.parameters.shape[-1]).reshape(-1, 2),
        #                method='L-BFGS-B')

        # 牛顿-共轭梯度法：Newton-CG
        res = minimize(self.fitness, self.parameters, method='nelder-mead')

        # 单纯形法：Nelder-Mead
        # res = minimize(self.fitness, self.parameters, method='BFGS')

        self.parameters = res.x
        matrix = self.corelation(self.gaussian, self.X, self.X, self.parameters) + 1e-8 * np.eye(len(self.X))
        self.inverse_matrix = np.linalg.inv(matrix)
        self.beta = self.F.dot(self.inverse_matrix).dot(self.Y) / (self.F.dot(self.inverse_matrix).dot(self.F.T))
        return self.inverse_matrix

    def predict(self, x_pre):
        # 相关向量
        vector = self.corelation(self.gaussian, self.X, x_pre, self.parameters)
        # 预测值
        y_pre = self.beta + vector.T.dot(self.inverse_matrix).dot(
            self.Y - self.F.dot(self.beta))
        return y_pre


if __name__ == "__main__":
    def curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    parameters = np.array([0.2])
    x_real = np.linspace(0, 1)
    y_real = curve(x_real)
    x_train = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    # x_train = np.array([0, 0.4, 0.6, 1])
    y_train = curve(x_train)
    print(y_real[-1])
    print(y_train[-1])

    kriging = Kriging(parameters=parameters)
    kriging.fit(x_train, y_train)

    x_pred = np.linspace(0, 1)
    y_pred = kriging.predict(x_pred)
    print(x_pred[-1])
    print(y_pred[-1])

    plt.plot(x_pred, y_pred, color='#00ffff', label='predicted value', linestyle='-')
    plt.plot(x_real, y_real, color='#ff0000', label='real value', linestyle='-')
    plt.scatter(x_train, y_train, color='#0000ff', label='train set', marker='s')
    plt.legend()
    # plt.show()
