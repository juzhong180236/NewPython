import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from ReadExcel import readExcel
import time


def gaussian(x, c, s):
    return np.exp(-(x - c) ** 2 / (2 * s ** 2))


def multiquadric(x, c, s):
    return np.sqrt((x - c) ** 2 + s ** 2)


def linear(x, c):
    return x - c


def linear_abs(x, c):
    return np.abs(x - c)


def square(x, c):
    return (x - c) ** 2


def cubic(x, c):
    return (x - c) ** 3


# def thinplatespline(x, c):
#     if x == 0:
#         return
#     return (x - c) ** 2 * np.log(np.abs(x - c))


def inversemultiquadric(x, c, s):
    return 1 / np.sqrt((x - c) ** 2 + s ** 2)


func = {"lin": linear, "cb": cubic, "sq": square, 'lin_a': linear_abs,
        "mq": multiquadric, "gs": gaussian, "imq": inversemultiquadric}
str_no_s = ['linear', 'cubic', 'square', 'linear_abs']


class RBF(object):
    # def RBF(X, Y, X_Pre):
    def __init__(self, rbf="mq", std=0, w=None, x=np.array([])):
        self.rbf = func[rbf]  # rbf名称
        self.std = std
        self.w = w
        self.x = x

    def fit(self, X, Y):
        list_result = []
        self.x = X
        # self.std = (max(X) - min(X)) / len(X)
        max_distance_list = []
        for i in range(X.shape[0]):
            max_distance_list.append(max([np.linalg.norm(m) for m in X - X[i]]))
        self.std = max(max_distance_list) / X.shape[0]
        for i in range(X.shape[0]):
            if self.rbf.__name__ in str_no_s:
                list_result.append(self.rbf(X[i], X).ravel())
            else:
                list_result.append(self.rbf(X[i], X, self.std).ravel())
        Gaussian_result = np.array(list_result)
        self.w = np.linalg.pinv(Gaussian_result).dot(Y)
        return ','.join(map(str, self.w))

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            if self.rbf.__name__ in str_no_s:
                list_pre_x.append(self.rbf(X_Pre[i], self.x).ravel())
            else:
                list_pre_x.append(self.rbf(X_Pre[i], self.x, self.std).ravel())
        Y_Pre = np.array(list_pre_x).dot(self.w)
        print(self.w.shape)
        print(self.std)
        print(np.array(list_pre_x).shape)
        return Y_Pre


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet1", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 1, 30, 2)
    start = time.perf_counter()
    d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    d_pred = np.arange(-17, 18)
    Y_pre = RBF('lin_a')
    Y_pre.fit(data_real[0], data_real[1])
    y_Pre = Y_pre.predict(data_pre[0])
    # RR = 1 - (np.sum(np.square(data_pre[1] - y_Pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # print(RR)
    Y_pre1 = RBF('lin_a')
    Y_pre1.fit(d, y)
    y_Pre1 = Y_pre1.predict(d_pred)
    # plt.plot(d, y, color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(data_pre[0], y_Pre, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')

    plt.plot(d, y, color='#ff0000', marker='+', linestyle='-',
             label='z-real')
    plt.plot(d_pred, y_Pre1, color='#0000ff', marker='+', linestyle='-.',
             label='z-predict')
    # RR = 1 - (np.sum(np.square(y - y_Pre1)) / np.sum(np.square(y - np.mean(y))))
    # print(RR)
    plt.legend()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)
