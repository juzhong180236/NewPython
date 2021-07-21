import numpy as np
from APP_utils.Algorithm.Surrogate_Model.PRS.PRS import PRS
import matplotlib.pyplot as plt


class LR_MFS(object):

    def __init__(self):
        self.dim = None
        self.X = None
        self.b = None
        pass

    def fit(self, XL, YL, XH, YH, xtest, degree):
        [mx, nx] = XH.shape
        self.dim = nx
        my = len(YH)
        if mx != my or mx < 2:
            ValueError("The size of training data are wrong!")
        [ms, ns] = xtest.shape
        if ns != nx:
            ValueError("The variables of xtr and xts should be the same!")
        prs = PRS(name="simple", m=9)
        prs.fit(XL, YL)
        # 求得测试点在低保真模型处的预测值
        YLtest = prs.predict(xtest).reshape(-1, 1)
        # print(YLtest)
        # 求高保真点在低保真模型处的值
        YL_H = prs.predict(XH).reshape(-1, 1)
        # print(YL_H)
        if degree == 1:
            self.X = np.hstack([YL_H, np.ones((mx, 1)), XH])
        else:
            self.X = np.hstack([YL_H, np.ones((mx, 1)), XH])
            for i in range(nx):
                self.X = [self.X, np.tile(XH[:, i], [1, nx - i + 1]) * XH[:, i: nx]]
        # print(np.linalg.inv(self.X.T.dot(self.X)))
        '''
        2021.06.21
        matlab版本的代码pinv是用的左除实现的。在matlab中，A\B相当于A的逆乘以B,但是当矩阵A接近奇异时，
        matlab的左除得到的结果和matlab自己的inv就不一样了，和python的inv也不一样。这导致最终结果不同。
        最重要的是matlab中的full mode对应的是python中的simple mode，所以刚开始遇见了求逆不一致问题。
        '''
        self.b = np.linalg.pinv(self.X.T.dot(self.X)).dot(self.X.T).dot(YH).reshape(-1, 1)
        # print(np.linalg.det(self.X.T.dot(self.X)))
        # print(self.X.T.dot(self.X))
        # print(np.linalg.inv(self.X.T.dot(self.X)).dot(self.X.T))
        rio = self.b[0, :].reshape(-1, 1)
        beta = self.b[1:, :].reshape(-1, 1)
        if degree == 1:
            Xts = np.hstack([np.ones((ms, 1)), xtest])
        else:
            Xts = np.hstack([np.ones((ms, 1)), xtest])
            for i in range(nx):
                Xts = [Xts, np.tile(xtest[:, i], [1, nx - i + 1]) * xtest[:, i: nx]]
        yhat_h = Xts.dot(beta) + YLtest.dot(rio)
        return yhat_h


if __name__ == "__main__":
    # # 第一次设置的测试函数
    # xl = np.arange(1, 11).reshape(-1, 2)
    # yl = xl[:, 0] + xl[:, 1] + 0.3
    # # print(yl)
    # xh = np.array([[1, 2], [4, 5], [9, 10]])
    # yh = xh[:, 0] + 0.3
    #
    # yh_l = xh[:, 0] + 0.3
    # xTest = np.array([[1, 3], [2, 3], [3, 3], [3, 5], [4, 5], [6, 5], [7, 6], [7, 8], [8, 9], [8, 10]])
    # lr_mfs = LR_MFS()
    # print(lr_mfs.fit(xl, yl, xh, yh, xTest, 1))

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
    # model_prs = PRS()
    # model_prs.fit(XL, YL)
    # # 求得测试点在低保真模型处的预测值
    # yyL = model_prs.predict(xtest)
    # yL_H = model_prs.predict(XH)
    # print(yyL)
    lr_mfs = LR_MFS()
    y_hat = lr_mfs.fit(XL, YL, XH, YH, xtest, 1)
    # print(y_hat)
    plt.plot(xtest, y_hat, color='r', linestyle='-', lw=2, label='predicted value')
    plt.plot(xtest, ytest, color='b', linestyle='--', lw=2, label='real value')
    plt.scatter(XH, YH, color='m', marker='s', lw=2, label='high fidelity train points')
    plt.scatter(XL, YL, color='g', marker='o', lw=2, label='low fidelity train points')
    plt.legend()
    plt.show()
    # # print(xl)
    # # print(yl)
    # # print(xh)
    # # print(yh)
    # # print(xTest)
