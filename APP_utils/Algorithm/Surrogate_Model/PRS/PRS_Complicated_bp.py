import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from mpl_toolkits.mplot3d import Axes3D
from ReadExcel import readExcel

class PRS(object):
    ''' 代理模型PRS

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

    def fit(self, X, Y, threshold):
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
        PRS_result = np.insert(np.array(list_PRS_result), 0, 1, axis=1)  # 所有元素的Gramian矩阵，将list转为ndarray
        # print(PRS_result)
        self.w = np.linalg.pinv(PRS_result).dot(Y)  # 根据Y和Gramian矩阵的伪逆求出权重w
        # print(self.w)
        w_remove = self.w
        PRS_result_remove = PRS_result
        min_element = -np.Inf
        while min_element < threshold:
            # print(PRS_result_remove[0])
            # 计算偏回归平方和loss，将公式拆解为四部分
            first = Y.dot(Y) - (w_remove.T.dot(PRS_result_remove.T)).dot(Y)
            second = Y.shape[0] - w_remove.shape[0]
            third = np.diag(np.linalg.inv(PRS_result_remove.T.dot(PRS_result_remove)))
            inner = first / second * third
            index_positive = np.where(inner > 0)  # 防止除数为零
            if inner[inner > 0].size == 0:
                break
            loss = w_remove / (np.maximum(inner, min(inner[inner > 0])) ** 0.5)

            min_element = min(np.abs(loss[index_positive]))
            # print(np.abs(loss[index_positive]))
            # print(min_element)
            remove_index = index_positive[0][np.where(np.abs(loss[index_positive]) == min_element)[0][0]]
            w_remove = np.delete(w_remove, remove_index, axis=0)
            PRS_result_remove = np.delete(PRS_result_remove, remove_index, axis=1)
        return w_remove, PRS_result_remove

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
        array_pre_x = np.insert(np.array(list_pre_x), 0, 1, axis=1)
        Y_Pre = array_pre_x.dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    path_excel = r"C:\Users\asus\Desktop\History\History_codes\NewPython\APP_utils\Algorithm\data\test7fun.xlsx"
    data_real = readExcel(path_excel, "Sheet1", 1, 20, 2)
    data_pre = readExcel(path_excel, "Sheet2", 1, 20, 2)
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    # y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
    # d_pred = np.arange(-17, 18)
    # dd = np.array(
    #     [[2, 3], [-5, -1], [1, 5], [9, 13], [9, 13], [9, 13], [9, 13], [9, 13], [9, 13], [9, 13], [9, 13], [9, 13],
    #      [9, 13], [9, 13], [9, 13], [9, 13]])
    # dy = np.array([55, 44, 88, 66, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88])
    # prs1 = PRS(m=3)
    # w = prs1.fit(dd, dy, 1)
    # first = dy.dot(dy) - (w[0].T.dot(w[1].T)).dot(dy)
    # second = dy.shape[0] - w[0].shape[0]
    # third = np.diag(np.linalg.inv(w[1].T.dot(w[1])))
    #
    # limian = first / second * third
    # # 大于0的元素，防止除数为0报错
    # d = np.where(limian > 0)
    #
    # ff = np.maximum(limian, min(limian[limian > 0])) ** 0.5
    # final = w[0] / ff
    # remove_index = d[0][np.where(final[d] == min(final[d]))[0][0]]
    #
    # new_Gramian = np.delete(w[1], remove_index, axis=1)
    # print(w[1])
    # print(new_Gramian)

    prs1 = PRS(m=3)
    # prs1.fit(data_real[0], data_real[1], 100)
    aa = prs1.fit(data_real[0], data_real[1], -np.Inf)
    Y_pre = prs1.predict(data_pre[0])
    # prs2 = PRS(m=7)
    # prs2.fit(d, y)
    # Y_pre1 = prs2.predict(d_pred)

    RR = 1 - (np.sum(np.square(data_pre[1] - Y_pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    print(RR)

    plt.plot(data_pre[0], data_pre[1], color='#ff0000', marker='+', linestyle='-',
             label='z-real')
    plt.plot(data_pre[0], Y_pre, color='#0000ff', marker='+', linestyle='-.',
             label='z-predict')

    # plt.plot(dd, dy, color='#ff0000', marker='+', linestyle='-',
    #          label='z-real')
    # plt.plot(d_pred, Y_pre1, color='#0000ff', marker='+', linestyle='-.',
    #          label='z-predict')
    plt.legend()
    plt.show()

    # data = np.random.randint(0, 255, size=[40, 40, 40])
    # fig = plt.figure()
    # x, y, z = data[0], data[1], data[2]
    # ax = fig.add_subplot(111, projection='3d')  # 创建一个三维的绘图工程
    #  将数据点分成三部分画，在颜色上有区分度
    # ax.scatter(dd[:, 0], dd[:, 1], dy, c='r')  # 绘制数据点

    # ax.set_xlabel('X')
    # plt.show()
