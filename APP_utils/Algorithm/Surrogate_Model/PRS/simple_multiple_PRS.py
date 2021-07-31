import numpy as np


class PRS(object):
    def __init__(self, m=2, w=0):
        self.m = m
        self.w = w

    def fit(self, X, Y):
        # 把训练点的x输入
        # data_PRS_result = np.empty(shape=(X.shape[0], self.m + 1), dtype=object)
        list_PRS_result = []
        for i in range(X.shape[0]):  # m
            # list_result = X[i]
            # list_combine = X[i]
            list_temp = []
            for j in range(self.m + 1):
                # list_temp = [ele * list_result for ele in X[i]]
                list_temp.append(X[i] ** j)
                # list_result = np.array(list_temp).flatten()
                # list_combine = np.concatenate((list_combine, list_result))
                # list_combine = np.hstack([list_combine, list_result])
                # data_PRS_result[i][j] = X[i] ** j
            list_PRS_result.append(np.array(list_temp).ravel())
        PRS_result = np.array(list_PRS_result)
        # print(PRS_result)
        # 根据Y和伪逆求出w
        self.w = np.linalg.pinv(PRS_result).dot(Y)
        return self.w.tolist()

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            list_result = X_Pre[i]
            list_combine = X_Pre[i]
            list_temp = []
            for j in range(self.m + 1):
                list_temp.append(X_Pre[i] ** j)
                # list_temp = [m * list_result for m in np.array(X_Pre[i])]
                # list_result = np.array(list_temp).flatten()
                # list_combine = np.concatenate((list_combine, list_result))
            # list_pre_x.append(list_combine)
            list_pre_x.append(np.array(list_temp).ravel())
        print(np.array(list_pre_x))
        Y_Pre = np.array(list_pre_x).dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    pass
