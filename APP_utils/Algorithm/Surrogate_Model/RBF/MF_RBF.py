import numpy as np
from APP_utils.Algorithm.Surrogate_Model.RBF.RBF_Surrogate import RBF
import matplotlib.pyplot as plt


class MF_RBF(object):

    def __init__(self):
        self.omega = None
        self.type = None
        self.sigma = None
        self.phi = None
        self.phis = None
        pass

    def __CoefGenerate_fix(self, xtest, xH, yL_H, yH, bf_type):
        ntrain = len(xH)
        dist = np.zeros((ntrain, ntrain))
        # print(xH[0])
        for i in range(ntrain):
            # 两个变量之差的平方
            dist1 = (xH - np.tile(xH[i, :], (ntrain, 1))) ** 2
            # 对上述的平方和求开方，如果是多维变量，则相加后再开方
            dist[i, :] = np.sqrt(np.sum(dist1, axis=1))
        #     print(dist1)
        # print(dist)

        if bf_type == 'LN':
            bf_sigma = 0
            phi = dist
        elif bf_type == 'CB':
            bf_sigma = 0
            phi = dist ** 3
        elif bf_type == 'TPS':
            bf_sigma = 0
            phi = dist ** 2 * np.log(dist)
        elif bf_type == 'G':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * ntrain)))
            phi = np.exp(-dist ** 2 / (2 * np.tile(bf_sigma ** 2, [ntrain, ntrain])))
        elif bf_type == 'MQ':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * ntrain)))
            phi = np.sqrt(dist ** 2 + np.tile(bf_sigma ** 2, [ntrain, ntrain]))
        elif bf_type == 'IMQ':
            bf_sigma = np.max(np.max(dist / np.sqrt(2 * ntrain)))
            phi = np.ones(ntrain) / np.sqrt(dist ** 2 + np.tile(bf_sigma ** 2, [ntrain, ntrain]))
        else:
            raise AttributeError("please input follow values: 'LN', 'CB', 'TSP', 'G', 'MQ', 'IMQ'.")
        # print(bf_sigma)
        # print(phi)
        # print(yL_H)
        Mphi = np.hstack((yL_H, phi))
        # print(Mphi)
        omega = Mphi.T.dot(np.linalg.inv(Mphi.dot(Mphi.T))).dot(yH)
        # print(omega)
        ntest = len(xtest)
        dists = np.zeros((ntest, ntrain))
        for i in range(ntest):
            dists1 = (xH - np.tile(xtest[i, :], (ntrain, 1))) ** 2
            dists[i, :] = np.sqrt(np.sum(dists1, axis=1))
        # print(dists)
        # Choose different basis function to generate Euclidean distance matrix
        if bf_type == 'LN':
            phis = dists
        elif bf_type == 'CB':
            phis = dists ** 3
        elif bf_type == 'TPS':
            phis = dists ** 2 * np.log(dists)
        elif bf_type == 'G':
            phis = np.exp(-dists ** 2 / (2 * np.tile(bf_sigma ** 2, [ntest, ntrain])))
        elif bf_type == 'MQ':
            phis = np.sqrt(dists ** 2 + np.tile(bf_sigma ** 2, [ntest, ntrain]))
        elif bf_type == 'IMQ':
            phis = np.ones((ntest, ntrain)) / np.sqrt(dists ** 2 + np.tile(bf_sigma ** 2, [ntest, ntrain]))
        else:
            raise AttributeError("please input follow values: 'LN', 'CB', 'TSP', 'G', 'MQ', 'IMQ'.")
        self.omega = omega
        self.type = bf_type
        self.sigma = bf_sigma
        self.phi = phi
        self.phis = phis
        # print(self.omega)
        # print(self.type)
        # print(self.sigma)
        # print(self.phi)
        # print(self.phis)

    def MFRBF_predict_fix(self, xtest, yyL, xH, yL_H, yH, bf_type):
        self.__CoefGenerate_fix(xtest, xH, yL_H, yH, bf_type)
        Mphis = np.hstack((yyL, self.phis))
        y_MFRBF = Mphis.dot(self.omega)
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
    model_rbf = RBF()
    model_rbf.fit(XL, YL)
    # 求得测试点在低保真模型处的预测值
    yyL = model_rbf.predict(xtest)
    yL_H = model_rbf.predict(XH)
    # print(yyL)
    mf_rbf = MF_RBF()
    y_hat = mf_rbf.MFRBF_predict_fix(xtest, yyL, XH, yL_H, YH, 'MQ')
    # print(y_hat)
    plt.plot(xtest, y_hat, color='r', linestyle='-', lw=2, label='predicted value')
    plt.plot(xtest, ytest, color='b', linestyle='--', lw=2, label='real value')
    plt.scatter(XH, YH, color='m', marker='s', lw=2, label='high fidelity train points')
    plt.scatter(XL, YL, color='g', marker='o', lw=2, label='low fidelity train points')
    plt.legend()
    plt.show()
