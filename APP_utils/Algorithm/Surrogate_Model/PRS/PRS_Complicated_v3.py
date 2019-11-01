import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from ReadExcel import readExcel


class PRS(object):
    ''' 代理模型PRS【没有常数项交叉】

        def __init__(self, m=3, w=0):
        初始化PRS类，默认次数取3，权重取0
        self.m = m
        self.w = w

        def fit(self, X, Y):
        根据X，Y数据进行训练
        参数：
            X: 给定数据的输入，一维或多维
            Y: 给定数据的输出，一维
        返回：
            返回self.w权重值

        def predict(self, X_Pre):
        根据fit方法训练的模型和X_Pre，预测相应的Y_Pre
        参数：
            X_Pre: 预测数据的输入值
        返回：
            Y_Pre: 预测的输出数据
    '''

    def __init__(self, m=7, w=0):
        self.m = m
        self.w = w

    def fit(self, X, Y):
        list_PRS_result = []  # 存放最终的Gramian矩阵的列表
        for i in range(X.shape[0]):  # 遍历输入值X的每个元素
            arr_result = X[i]  # 输入值X的每一个元素的在每一次m（次数）的Gramian矩阵
            arr_combine = X[i]  # 输入值X的每一个元素经过m（次数）次合并的Gramian矩阵
            list_index = list(range(1, X.shape[-1] + 1))
            list_index.reverse()  # 得到初始的每一次m时的Gramian矩阵的每一行元素个数，初始为3,2,1
            for j in range(self.m):  # 遍历输入值X的每个元素个次数m
                list_temp = []  # 数据与arr_result一样，类型为list
                for h in range(X.shape[-1]):  # 遍历输入值X的每个元素的每个维度
                    # print("当前Gramian矩阵的第" + str(h) + "行:" + str(list_result[-list_index[h]:len(list_result)]))
                    # x1*(x1,x2,x3), x2*(x2,x3), x3*(x3), 类似这样的式子，根据list_index中的元素，从后往前取
                    list_temp.extend(X[i][h] * arr_result[-list_index[h]:len(arr_result)])
                    # 更新list_index中的元素，更新后的list第一个元素为原list所有元素相加，第二个元素为原list去掉第一个元素后所有元素相加，以此类推
                    list_index[h] = sum(list_index[h:])
                arr_result = np.array(list_temp)  # 将list转为ndarray
                arr_combine = np.concatenate((arr_combine, arr_result))  # 将ndarray组合起来作为每个元素的Gramian矩阵
                # print("当前的Gramian矩阵:" + str(list_combine))
            list_PRS_result.append(arr_combine)  # 每个元素的Gramian矩阵
        PRS_result = np.array(list_PRS_result)  # 所有元素的Gramian矩阵，将list转为ndarray
        self.w = np.linalg.pinv(PRS_result).dot(Y)  # 根据Y和Gramian矩阵的伪逆求出权重w
        return self.w

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            list_result = X_Pre[i]
            list_combine = X_Pre[i]
            list_index = list(range(1, X_Pre.shape[-1] + 1))
            list_index.reverse()
            for j in range(self.m):
                list_temp = []
                for h in range(X_Pre.shape[-1]):
                    list_temp.extend(X_Pre[i][h] * list_result[-list_index[h]:len(list_result)])
                    list_index[h] = sum(list_index[h:])
                list_result = np.array(list_temp).flatten()
                list_combine = np.concatenate((list_combine, list_result))
            list_pre_x.append(list_combine)
        Y_Pre = np.array(list_pre_x).dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet1", 1, 30, 3)
    data_pre = readExcel(path_excel, "Sheet2", 1, 30, 3)
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    # y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    # d_pred = np.arange(-17, 18)
    # dd = np.array([[2, 3, 2], [-5, -1, 0], [1, 5, 7], [9, 13, 17]])
    # dy = np.array([55, 44, 88, 66])
    # prs1 = PRS(m=3)
    # prs1.fit(dd, dy)

    prs1 = PRS(m=3)
    prs1.fit(data_real[0], data_real[1])
    Y_pre = prs1.predict(data_pre[0])

    # prs2 = PRS(m=7)
    # prs2.fit(d, y)
    # Y_pre1 = prs2.predict(d_pred)

    # RR = 1 - (np.sum(np.square(data_pre[1] - Y_pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # print(RR)

    # plt.plot(data_pre[0], data_pre[1], color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(data_pre[0], Y_pre, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')

    # plt.plot(d, y, color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(d_pred, Y_pre1, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')

    # plt.legend()
    # plt.show()
