import numpy as np
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF_Surrogate import RBF
import matplotlib.pyplot as plt


class MF_RBF(object):

    def __init__(self):
        self.omega = None
        self.rbf_type = None
        self.bf_sigma = None
        self.phi = None
        self.phis = None
        self.y_x_low_by_low_model = None
        self.low_model = None
        self.y_x_high_by_low_model = None
        self.x_high = None
        self.y_high = None

    def fit(self, x_low, y_low, x_high, y_high, bf_type="MQ"):
        self.x_high = x_high
        self.y_high = y_high
        self.low_model = RBF(rbf="gs")
        self.low_model.fit(x_low, y_low)
        # print(np.asarray([12.5, 0]).reshape(1, -1))
        # print(self.low_model.predict(np.asarray([12.5, 0]).reshape(1, -1)))
        self.y_x_high_by_low_model = self.low_model.predict(x_high)
        n_train = len(self.x_high)
        dist = np.zeros((n_train, n_train))
        for i in range(n_train):
            # 两个变量之差的平方
            dist1 = (x_high - np.tile(x_high[i, :], (n_train, 1))) ** 2
            # 对上述的平方和求开方，如果是多维变量，则相加后再开方
            dist[i, :] = np.sqrt(np.sum(dist1, axis=1))

        if bf_type == 'LN':
            bf_sigma = 0
            phi = dist
        elif bf_type == 'CB':
            bf_sigma = 0
            phi = dist ** 3
        elif bf_type == 'TPS':
            bf_sigma = 0
            phi = dist ** 2. * np.log(dist)
        elif bf_type == 'G':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * n_train)))
            phi = np.exp(-dist ** 2. / (2 * np.tile(bf_sigma ** 2, [n_train, n_train])))
        elif bf_type == 'MQ':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * n_train)))
            phi = np.sqrt(dist ** 2 + np.tile(bf_sigma ** 2, [n_train, n_train]))
        elif bf_type == 'IMQ':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * n_train)))
            phi = np.ones(n_train) / np.sqrt(dist ** 2 + np.tile(bf_sigma ** 2, [n_train, n_train]))
        else:
            raise AttributeError("please input follow values: 'LN', 'CB', 'TSP', 'G', 'MQ', 'IMQ'.")
        Mphi = np.hstack((self.y_x_high_by_low_model, phi))
        omega = Mphi.T.dot(np.linalg.inv(Mphi.dot(Mphi.T))).dot(y_high)

        self.omega = omega
        self.rbf_type = bf_type
        self.bf_sigma = bf_sigma
        self.phi = phi

    def predict(self, x_test):
        # x_test = np.asarray([[12.5, 0]])
        self.y_x_low_by_low_model = self.low_model.predict(x_test)
        n_train = len(self.x_high)
        n_test = len(x_test)
        dists = np.zeros((n_test, n_train))
        # print(x_test)
        # print(np.tile(x_test[0, :], (n_train, 1)))
        for i in range(n_test):
            dists1 = (self.x_high - np.tile(x_test[i, :], (n_train, 1))) ** 2
            dists[i, :] = np.sqrt(np.sum(dists1, axis=1))
        # Choose different basis function to generate Euclidean distance matrix
        if self.rbf_type == 'LN':
            phis = dists
        elif self.rbf_type == 'CB':
            phis = dists ** 3
        elif self.rbf_type == 'TPS':
            phis = dists ** 2. * np.log(dists)
        elif self.rbf_type == 'G':
            phis = np.exp(-dists ** 2. / (2 * np.tile(self.bf_sigma ** 2, [n_test, n_train])))
        elif self.rbf_type == 'MQ':
            phis = np.sqrt(dists ** 2 + np.tile(self.bf_sigma ** 2, [n_test, n_train]))
        elif self.rbf_type == 'IMQ':
            phis = np.ones(n_train) / np.sqrt(dists ** 2 + np.tile(self.bf_sigma ** 2, [n_test, n_train]))
        else:
            raise AttributeError("please input follow values: 'LN', 'CB', 'TSP', 'G', 'MQ', 'IMQ'.")
        # 求得测试点在低保真模型处的预测值 动态预测
        self.phis = phis
        # 只需要知道 yyL phis omega 就可以进行预测
        # 而在这之前，XL,YL,XH yL_H YH 'MQ' 可固化 xtest yyL 动态
        # print(self.y_x_low_by_low_model)
        # print(self.phis)
        Mphis = np.hstack((self.y_x_low_by_low_model, self.phis))
        # print(Mphis)
        y_MFRBF = Mphis.dot(self.omega)
        # print(y_MFRBF)

        return y_MFRBF


if __name__ == "__main__":
    A_value = 0.5
    B_value = 10
    C_value = -5


    # 高保真的曲线函数表达式
    def onevar(x):
        return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


    # 高保真的曲线函数表达式
    def cheaponevar(x, A=A_value, B=B_value, C=C_value):
        return A * onevar(x) + B * (x - 0.5) + C


    XL = np.linspace(0, 1, 11).reshape(-1, 1)
    YL = cheaponevar(XL)
    XH = np.asarray([0, 0.4, 0.6, 0.8, 1]).reshape(-1, 1)
    YH = onevar(XH)
    xtest = np.linspace(0, 1, 101).reshape(-1, 1)
    ytest = onevar(xtest)
    ntest = len(ytest)
    xtrain = XH
    ytrain = YH
    ntrain = len(YH)

    # 用低保真点拟合低保真模型
    # model_rbf = RBF()
    # model_rbf.fit(XL, YL)
    # 求得测试点在低保真模型处的预测值 动态预测
    # yyL = model_rbf.predict(xtest)
    # 求得高保真点在低保真模型的值 可固化
    # yL_H = model_rbf.predict(XH)
    mf_rbf = MF_RBF()
    # XH yL_H YH 'MQ' 可固化 xtest yyL 动态
    mf_rbf.fit(XL, YL, XH, YH, 'MQ')
    y_hat = mf_rbf.predict(xtest)
    # print(y_hat)
    plt.plot(xtest, y_hat, color='r', linestyle='-', lw=2, label='predicted value')
    plt.plot(xtest, ytest, color='b', linestyle='--', lw=2, label='real value')
    plt.scatter(XH, YH, color='m', marker='s', lw=2, label='high fidelity train points')
    plt.scatter(XL, YL, color='g', marker='o', lw=2, label='low fidelity train points')
    plt.legend()
    plt.show()
