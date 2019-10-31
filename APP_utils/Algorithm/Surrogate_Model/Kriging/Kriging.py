import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from ReadExcel import readExcel


def Gaussian(x, c, s):
    return np.exp(-(x - c) ** 2 / (2 * s ** 2))


def Multiquadric(x, c, s):
    return np.sqrt((x - c) ** 2 + s ** 2)


class Kriging(object):
    def __init__(self, rbf=Multiquadric, std=0, w=0):
        self.rbf = rbf  # rbf名称
        self.std = std
        self.w = w

    def fit(self, X, Y):
        list__result = []
        distance_list = []
        semivariance_list = []
        self.x = X
        for i in range(X.shape[0]):
            distance_list.append([np.linalg.norm(ele) for ele in X - X[i]])
            semivariance_list.append([ele ** 2 for ele in Y - Y[i]])
        distance_array = np.array(distance_list).flatten()
        semivariace_array = np.array(semivariance_list).flatten()
        return distance_array, semivariace_array
        # print(X - X[i])
        # print(Y - Y[i])
        # print(len(distance_list))
        # print(distance_list)
        # print(semivariance_list)
    #         list_temp = []
    #         for j in range(X.shape[0]):
    #             list_temp.append(self.rbf(X[i], X[j], self.std))
    #         list__result.append(np.array(list_temp).ravel())
    #     Gaussian_result = np.array(list__result)
    #     self.w = np.linalg.pinv(Gaussian_result).dot(Y)
    #     return ','.join(map(str, self.w))
    #
    # def predict(self, X_Pre):
    #     list_pre_x = []
    #     for i in range(X_Pre.shape[0]):
    #         list_temp = []
    #         for j in range(self.x.shape[0]):
    #             list_temp.append(self.rbf(X_Pre[i], self.x[j], self.std))
    #         list_pre_x.append(np.array(list_temp).ravel())
    #     Y_Pre = np.array(list_pre_x).dot(self.w)
    #     return Y_Pre


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet1", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 1, 30, 2)
    dd = np.array([[2, 3], [-5, -1], [1, 5], [9, 13]])
    dy = np.array([55, 44, 88, 66])
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    # y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    # d_pred = np.arange(-17, 18)

    Y_pre1 = Kriging()
    x1, y1 = Y_pre1.fit(data_real[0], data_real[1])
    plt.scatter(x1, y1, c='#ff0000', s=30, label='dot', alpha=0.6, edgecolors='black')
    # y_Pre1 = Y_pre1.predict(d_pred)
    # plt.plot(x1, y1, color='#ff0000', marker='+',
    #          label='z-real')
    # plt.plot(data_pre[0], y_Pre, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')

    # RR = 1 - (np.sum(np.square(y - y_Pre1)) / np.sum(np.square(y - np.mean(y))))
    # print(RR)
    plt.legend()
    plt.show()
