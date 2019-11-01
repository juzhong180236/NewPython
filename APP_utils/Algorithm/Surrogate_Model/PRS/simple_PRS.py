import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from ReadExcel import readExcel


class PRS(object):
    def __init__(self, m=7, w=0):
        self.m = m
        self.w = w

    def fit(self, X, Y):
        # 把训练点的x输入
        # data_PRS_result = np.empty(shape=(X.shape[0], self.m + 1), dtype=object)
        list_PRS_result = []
        for i in range(X.shape[0]):
            list_temp = []
            for j in range(self.m + 1):
                list_temp.append(X[i] ** j)
                # data_PRS_result[i][j] = X[i] ** j
            list_PRS_result.append(np.array(list_temp).ravel())
        PRS_result = np.array(list_PRS_result)
        # 根据Y和伪逆求出w
        self.w = np.linalg.pinv(PRS_result).dot(Y)
        return self.w

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            list_temp = []
            for j in range(self.m + 1):
                list_temp.append(X_Pre[i] ** j)
            list_pre_x.append(np.array(list_temp).ravel())
        Y_Pre = np.array(list_pre_x).dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet1", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 1, 30, 2)
    d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    d_pred = np.arange(-17, 18)
    # Y_pre = PRS(d_duo, 3, y_duo, d_pred_duo)
    # prs1 = PRS(m=4)
    # prs1.fit(data_real[0], data_real[1])
    # Y_pre = prs1.predict(data_pre[0])

    prs2 = PRS(m=7)
    prs2.fit(d, y)
    Y_pre1 = prs2.predict(d_pred)

    # RR = 1 - (np.sum(np.square(d_pred[1] - Y_pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # print(RR)

    plt.plot(d, y, color='#ff0000', marker='+', linestyle='-',
             label='z-real')
    plt.plot(d_pred, Y_pre1, color='#0000ff', marker='+', linestyle='-.',
             label='z-predict')

    # plt.plot(data_pre[0], data_pre[1], color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(data_pre[0], Y_pre, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')

    plt.legend()
    plt.show()
