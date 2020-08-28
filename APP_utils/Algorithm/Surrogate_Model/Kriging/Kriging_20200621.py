import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from GPR import GPR
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

    def gaussian(self, para_list, X1, X2):
        if X2.ndim != 1:
            return np.prod(np.exp(-para_list[0] * (np.abs(X1 - X2) ** para_list[1])), axis=-1)
        else:
            return np.exp(-para_list[0] * (np.abs(X1 - X2) ** para_list[1]))

    def corelation(self, func, X, Y, para_array):
        list_result = []
        # print(X.shape[0])
        for i in range(X.shape[0]):
            if para_array.shape[-1] == 3:
                list_result.append(para_array[2] * func(para_array, X[i], Y).ravel())
            else:
                list_result.append(func(para_array, X[i], Y).ravel())
        # print(np.array(list_result))
        return np.array(list_result)

    def fitness(self, parameters):
        self.parameters = parameters
        # print(self.parameters)

        matrix = self.corelation(self.gaussian, self.X, self.X, self.parameters) + 1e-8 * np.eye(len(self.X))
        # print(matrix)
        inverse_matrix = np.linalg.inv(matrix)
        # 均值
        self.beta = self.F.T.dot(inverse_matrix).dot(self.Y) / (self.F.T.dot(inverse_matrix).dot(self.F))
        # 方差
        self.sigma2 = ((self.Y - self.F.dot(self.beta)).T.dot(inverse_matrix).dot(self.Y - self.F.dot(self.beta))) / \
                      self.F.shape[-1]
        R = np.abs(np.linalg.det(matrix))
        # self.sigma2 = np.finfo(np.float64).tiny if self.sigma2 == 0 else self.sigma2
        return np.log(np.abs(self.sigma2)) * (self.F.shape[-1] / 2) + 1 / 2 * np.log(R)

    def fit(self, X, Y):
        self.X = np.asarray(X)
        self.Y = np.asarray(Y)
        # print(self.corelation(self.gaussian, self.X, self.X, self.parameters))
        self.F = np.ones(X.shape[-1])
        # 牛顿-共轭梯度法：Newton-CG
        # 拟牛顿法：BFGS

        # 单纯形法：Nelder-Mead
        # res = minimize(self.fitness, self.parameters,
        #                bounds=np.array([1e-4, 1e4] * self.parameters.shape[-1]).reshape(-1, 2),
        #                method='L-BFGS-B')
        res = minimize(self.fitness, self.parameters, method='nelder-mead')
        self.parameters = res.x
        print(self.parameters)

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
    # parameter_array_c = np.array([0.2, 2])
    #
    # x_real = np.linspace(0, 10)
    # y_real = np.cos(x_real)
    #
    # x_train = np.array([0.3, 3, 5, 8, 10])
    # y_train = np.cos(x_train)
    #
    # x_pred = np.linspace(0, 10)
    #
    # kriging = Kriging(parameters=parameter_array_c)
    # kriging.fit(x_train, y_train)
    #
    # y_pred = kriging.predict(x_pred)
    # plt.plot(x_real, y_real, color='#0000ff', label='real', linestyle='-')
    # plt.scatter(x_train, y_train, color='#0000ff', label='point', marker='s')
    #
    # plt.plot(x_pred, y_pred, color='#ff0000', label='krig-predict', linestyle=':')
    #
    # gpr = GPR()
    # gpr.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
    # ye_pred = gpr.predict(x_pred.reshape(-1, 1))
    # plt.plot(x_pred, ye_pred, color='#000000', label='gpr-predict', linestyle=':')
    #
    # # print('theta和p的最优解分别是:', kriging.parameters)
    # # print('最优目标函数值:', value)
    # plt.legend()
    # plt.show()

    A_value = 0.5
    B_value = 10
    C_value = -5

    parameter_array_c = np.array([0.2, 2])

    x_real = np.linspace(0, 1)

    x_pred = np.linspace(0, 1)
    x_pred1 = np.arange(0, 1.1, 0.1)


    # print(x_pred)
    # print(x_pred1)

    def high_fidelity_curve(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    def low_fidelity_curve(x, A=A_value, B=B_value, C=C_value):
        return A * high_fidelity_curve(x) + B * (x - 0.5) + C


    XC_point = np.array([0, 0.4, 0.6, 1])
    YC_point = high_fidelity_curve(XC_point)

    y_real = high_fidelity_curve(x_real)

    C_krig = Kriging(parameters=parameter_array_c)
    C_krig.fit(XC_point, YC_point)
    y_pre_c = C_krig.predict(x_pred)

    plt.plot(x_pred, y_pre_c, color='#00ffff', label='real', linestyle='-')
    plt.plot(x_real, y_real, color='#ff0000', label='real', linestyle='-')
    plt.scatter(XC_point, YC_point, color='#0000ff', label='point', marker='s')

    plt.show()
