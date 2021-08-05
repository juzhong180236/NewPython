import numpy as np


class PRS(object):
    def __init__(self, m=3, w=0):
        self.m = m
        self.w = w
        self.gram_matrix = None

    def calc_gram_matrix(self, X):
        list_PRS_result = []
        for i in range(X.shape[0]):  # m
            list_temp = []
            for j in range(self.m + 1):
                list_temp.append(X[i] ** j)
            list_PRS_result.append(np.array(list_temp).ravel())
        self.gram_matrix = np.array(list_PRS_result)
        return self.gram_matrix

    def fit(self, Y):
        # self.w = np.linalg.solve(self.gram_matrix, Y)
        self.w = np.linalg.pinv(self.gram_matrix).dot(Y)
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
        Y_Pre = np.array(list_pre_x).dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    pass
