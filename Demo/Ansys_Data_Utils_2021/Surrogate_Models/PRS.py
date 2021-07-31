import APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS as bp_com
import APP_utils.Algorithm.Surrogate_Model.PRS.simple_PRS as simple
import APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS as simple_m
import APP_utils.Algorithm.Surrogate_Model.PRS.stepwise_complicated_PRS as sw_com
import numpy as np
import matplotlib.pyplot as plt


class PRS(object):
    """ 代理模型PRS【bp、有/无常数项交叉、】

        def __init__(self, name='full'):
        选择PRS类，默认为有交叉项
        ['full', 'bp', 'zi', 'simple', 'simple_m', 'stepwise']分别为
        有交叉项，向后传播，截距为零，无交叉项一维，无交叉项多维，逐步回归
        self.name = name
        self.prs = None
    """

    def __init__(self, name='simple', m=2):
        self.name = name
        self.m = m
        self.prs = None
        if self.name in ['full', 'bp', 'zi']:
            self.prs = bp_com.PRS(name=self.name, m=self.m)
        elif self.name == 'simple':
            self.prs = simple.PRS(m=self.m)
        elif self.name == 'simple_m':
            self.prs = simple_m.PRS(m=self.m)
        elif self.name == 'stepwise':
            self.prs = sw_com.PRS(m=self.m)
        else:
            self.prs = None
            # 有其他的继续往下加

    def fit(self, X, Y):
        return self.prs.fit(X, Y)

    def predict(self, X_Pre):
        return self.prs.predict(X_Pre)


if __name__ == "__main__":
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])

    x_real = np.arange(-17, 18, 0.1)
    y_real = np.sin(x_real)

    x_train = np.arange(-17, 21, 3)
    y_train = np.sin(x_train)

    x_pred = np.arange(-17, 18, 0.1)

    rbf = PRS('stepwise')

    rbf.fit(x_train, y_train)

    y_pred = rbf.predict(x_pred)
    # RR = 1 - (np.sum(np.square(data_pre[1] - y_Pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # print(RR)
    plt.plot(x_real, y_real, color='#ff0000', linestyle='-', label='real')
    plt.plot(x_pred, y_pred, color='#0000ff', linestyle=':', label='predict')
    plt.scatter(x_train, y_train, color='#000000', label='point', marker='s')
    # RR = 1 - (np.sum(np.square(y - y_Pre1)) / np.sum(np.square(y - np.mean(y))))
    # print(RR)
    plt.legend()
    plt.show()
