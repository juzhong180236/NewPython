import numpy as np


class PRS(object):
    ''' 代理模型PRS【bp、有/无常数项交叉、】

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

    def __init__(self, name='full', threshold=1, m=2, w=0, remove_index=None):
        if remove_index is None:
            remove_index = []
        self.name = name
        if self.name in ['full', 'zi']:
            self.threshold = -np.Inf
        elif self.name == 'bp':
            self.threshold = threshold
        self.m = m
        self.w = w
        self.remove_index = remove_index
        self.gram_matrix = None

    def calc_gram_matrix(self, X):
        list_PRS_result = []  # 存放最终的Gramian矩阵的列表
        for i in range(X.shape[0]):  # 遍历输入值X的每个元素
            arr_result = X[i]  # 输入值X的每一个元素的在每一次m（次数）的Gramian矩阵
            arr_combine = X[i]  # 输入值X的每一个元素经过m（次数）次合并的Gramian矩阵
            list_index = list(range(1, X.shape[-1] + 1))
            list_index.reverse()  # 得到初始的每一次m时的Gramian矩阵的每一行元素个数，初始为3,2,1
            for j in range(self.m - 1):  # 遍历输入值X的每个元素个次数m
                list_temp = []  # 数据与arr_result一样，类型为list
                for h in range(X.shape[-1]):  # 遍历输入值X的每个元素的每个维度
                    # print("当前Gramian矩阵的第" + str(h) + "行:" + str(list_result[-list_index[h]:len(list_result)]))
                    # x1*(x1,x2,x3), x2*(x2,x3), x3*(x3), 类似这样的式子，根据list_index中的元素，从后往前取
                    list_temp.extend(X[i][h] * arr_result[-list_index[h]:len(arr_result)])
                    # 更新list_index中的元素，更新后的list第一个元素为原list所有元素相加，第二个元素为原list去掉第一个元素后所有元素相加，以此类推
                    list_index[h] = sum(list_index[h:])
                arr_result = np.array(list_temp)  # 将list转为ndarray
                # arr_combine = np.concatenate((arr_combine, arr_result))  # 将ndarray组合起来作为每个元素的Gramian矩阵
                arr_combine = np.hstack([arr_combine, arr_result])  # 将ndarray组合起来作为每个元素的Gramian矩阵
                # print("当前的Gramian矩阵:" + str(list_combine))
            list_PRS_result.append(np.hstack([[1] * X.shape[-1], arr_combine]))  # 每个元素的Gramian矩阵
        if self.m == 0:
            self.gram_matrix = np.array([1] * X.shape[-1]).reshape(-1, 1)
        else:
            self.gram_matrix = np.delete(np.array(list_PRS_result), range(X.shape[-1] - 1), axis=1)
        if self.name == 'zi':
            self.gram_matrix = np.delete(self.gram_matrix, 0, axis=1)  # 所有元素的Gramian矩阵，将list转为ndarray
        return self.gram_matrix

    def fit(self, Y):
        # self.w = np.linalg.solve(self.gram_matrix, Y)
        self.w = np.linalg.pinv(self.gram_matrix).dot(Y)  # 根据Y和Gramian矩阵的伪逆求出权重w
        min_element = -np.Inf
        while min_element < self.threshold:
            # print(PRS_result_remove[0])
            # 计算偏回归平方和loss，将公式拆解为四部分
            first = Y.dot(Y) - (self.w.T.dot(self.gram_matrix.T)).dot(Y)
            second = Y.shape[0] - self.w.shape[0]
            third = np.diag(np.linalg.inv(self.gram_matrix.T.dot(self.gram_matrix)))
            inner = first / second * third
            index_positive = np.where(inner > 0)  # 防止除数为零
            if inner[inner > 0].size == 0:
                return self.w, self.gram_matrix
            loss = self.w / (np.maximum(inner, min(inner[inner > 0])) ** 0.5)
            min_element = min(np.abs(loss[index_positive]))
            remove_index = index_positive[0][np.where(np.abs(loss[index_positive]) == min_element)[0][0]]
            self.remove_index.append(remove_index)
            self.w = np.delete(self.w, remove_index, axis=0)
            self.gram_matrix = np.delete(self.gram_matrix, remove_index, axis=1)
        return self.w.tolist()

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            list_result = X_Pre[i]
            list_combine = X_Pre[i]
            list_index = list(range(1, X_Pre.shape[-1] + 1))
            list_index.reverse()
            for j in range(self.m - 1):
                list_temp = []
                for h in range(X_Pre.shape[-1]):
                    list_temp.extend(X_Pre[i][h] * list_result[-list_index[h]:len(list_result)])
                    list_index[h] = sum(list_index[h:])
                list_result = np.array(list_temp).flatten()
                list_combine = np.hstack([list_combine, list_result])
            list_pre_x.append(np.hstack([[1] * X_Pre.shape[-1], list_combine]))
        if self.m == 0:
            array_pre_x = np.array([1] * X_Pre.shape[-1]).reshape(-1, 1)
        else:
            array_pre_x = np.delete(np.array(list_pre_x), range(X_Pre.shape[-1] - 1), axis=1)
        if self.name == 'zi':
            array_pre_x = np.delete(array_pre_x, 0, axis=1)
        for index in self.remove_index:
            array_pre_x = np.delete(array_pre_x, index, axis=-1)
        Y_Pre = array_pre_x.dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    pass
