import bp_complicated_PRS as bp_com
import simple_PRS as simple
import simple_multiple_PRS as simple_m
import stepwise_complicated_PRS as sw_com
import numpy as np
from ReadExcel import readExcel
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
    def __init__(self, name='full'):
        self.name = name
        self.prs = None
        if self.name in ['full', 'bp', 'zi']:
            self.prs = bp_com.PRS(self.name)
        elif self.name == 'simple':
            self.prs = simple.PRS(self.name)
        elif self.name == 'simple_m':
            self.prs = simple_m.PRS(self.name)
        elif self.name == 'stepwise':
            self.prs = sw_com.PRS(self.name)
            # 有其他的继续往下加

    def fit(self, X, Y):
        self.prs.fit(X, Y)

    def predict(self, X_Pre):
        return self.prs.predict(X_Pre)


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet2", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 30, 60, 2)
    prs1 = PRS('stepwise')
    prs1.fit(data_real[0], data_real[1])
    Y_pre = prs1.predict(data_pre[0])

    RR = 1 - (np.sum(np.square(data_pre[1] - Y_pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    print(RR)

    plt.plot(data_pre[0], data_pre[1], color='#ff0000', marker='+', linestyle='-',
             label='z-real')
    plt.plot(data_pre[0], Y_pre, color='#0000ff', marker='+', linestyle='-.',
             label='z-predict')

    plt.legend()
    plt.show()
