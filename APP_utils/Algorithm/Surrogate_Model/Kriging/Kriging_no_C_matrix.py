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
        self.Yc_Xe = None
        self.C_matrix = None

    def gaussian(self, para_list, X1, X2):
        if X2.ndim != 1:
            return np.prod(np.exp(-para_list[0] * (np.abs(X1 - X2) ** 2)), axis=-1)
        else:
            return np.exp(-para_list[0] * (np.abs(X1 - X2) ** 2))

    def corelation(self, func, X, Y, para_array):
        list_result = []
        for i in range(X.shape[0]):
            list_result.append(func(para_array, X[i], Y).ravel())
        # print(np.array(list_result))
        return np.array(list_result)

    def fitness(self, parameters):
        self.parameters = parameters
        # print(self.parameters)

        matrix = self.corelation(self.gaussian, self.X, self.X, self.parameters) + 1e-8 * np.eye(len(self.X))
        inverse_matrix = np.linalg.inv(matrix)
        # if self.parameters.shape[-1] == 2:
        if self.Yc_Xe is not None:
            d = self.Y - self.parameters[1] * self.Yc_Xe
            # d = self.Y
            self.beta = self.F.T.dot(inverse_matrix).dot(d) / (self.F.T.dot(inverse_matrix).dot(self.F))
            # 方差
            self.sigma2 = ((d - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(d - self.F.dot(self.beta))) / \
                          self.F.shape[-1]
        else:
            # 均值
            self.beta = self.F.T.dot(inverse_matrix).dot(self.Y) / (self.F.T.dot(inverse_matrix).dot(self.F))
            # 方差
            self.sigma2 = ((self.Y - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(self.Y - self.F.dot(self.beta))) / \
                          self.F.shape[-1]
        R = np.abs(np.linalg.det(matrix))
        # self.sigma2 = np.finfo(np.float64).tiny if self.sigma2 == 0 else self.sigma2
        return np.log(np.abs(self.sigma2)) * (self.F.shape[-1] / 2) + 1 / 2 * np.log(R)

    def fit(self, X, Y, Yc_Xe=None):
        if Yc_Xe is not None:
            self.Yc_Xe = Yc_Xe
        self.X = np.asarray(X)
        self.Y = np.asarray(Y)
        # print(self.corelation(self.gaussian, self.X, self.X, self.parameters))
        self.F = np.ones(X.shape[-1])
        # 拟牛顿法：BFGS
        # 未知方法
        # res = minimize(self.fitness, self.parameters,
        #                bounds=np.array([1e-4, 1e4] * self.parameters.shape[-1]).reshape(-1, 2),
        #                method='L-BFGS-B')

        # 牛顿-共轭梯度法：Newton-CG
        # res = minimize(self.fitness, self.parameters, method='nelder-mead')

        # 单纯形法：Nelder-Mead
        res = minimize(self.fitness, self.parameters, method='BFGS')

        self.parameters = res.x
        # print(self.parameters)

        matrix = self.corelation(self.gaussian, self.X, self.X, self.parameters) + 1e-8 * np.eye(len(self.X))
        self.inverse_matrix = np.linalg.inv(matrix)
        self.beta = self.F.dot(self.inverse_matrix).dot(self.Y) / (self.F.dot(self.inverse_matrix).dot(self.F.T))
        return self.inverse_matrix

    def predict(self, X_pre):
        # 相关向量
        vector = self.corelation(self.gaussian, self.X, X_pre, self.parameters)
        # 预测值
        Y_pre = self.beta + vector.T.dot(self.inverse_matrix).dot(
            self.Y - self.F.dot(self.beta))
        return Y_pre


if __name__ == "__main__":
    A_value = 0.5
    B_value = 10
    C_value = -5
    parameter_array_c = np.array([0.2])
    x_real = np.linspace(0, 1)
    x_pred = np.linspace(0, 1)
    x_pred1 = np.arange(0, 1.1, 0.1)


    def high_fidelity_curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    def low_fidelity_curve(x, A=A_value, B=B_value, C=C_value):
        return A * high_fidelity_curve(x) + B * (x - 0.5) + C


    XC_point = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    YC_point = low_fidelity_curve(XC_point)
    y_real = low_fidelity_curve(x_real)
    C_krig = Kriging(parameters=parameter_array_c)
    C_krig.fit(XC_point, YC_point)
    y_pre_c = C_krig.predict(x_pred)

    plt.plot(x_pred, y_pre_c, color='#00ffff', label='predicted value', linestyle='-')
    plt.plot(x_real, y_real, color='#ff0000', label='real value', linestyle='-')
    plt.scatter(XC_point, YC_point, color='#0000ff', label='point', marker='s')
    plt.legend()
    plt.show()
