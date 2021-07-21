import numpy as np
import matplotlib.pyplot as plt
import time


def gaussian(x, c, s):
    if c.ndim != 1:
        return np.sum(np.exp(-np.sqrt(np.sum((x - c) ** 2, axis=-1)) / (2 * s ** 2)), axis=-1)
    else:
        return np.exp(-(x - c) ** 2 / (2 * s ** 2))


def multiquadric(x, c, s):
    if c.ndim != 1:
        return np.sqrt(np.sqrt(np.sum((x - c) ** 2, axis=-1)) + s ** 2)
    else:
        return np.sqrt((x - c) ** 2 + s ** 2)


def linear(x, c):
    return x - c


def linear_abs(x, c):
    if c.shape[-1] != 1:
        return np.sum(np.abs(np.sqrt(np.sum((x - c) ** 2, axis=-1))), axis=-1)
    else:
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
    def __init__(self, rbf="mq", std=0, w=0, x=np.array([])):
        self.rbf = func[rbf]  # rbf的基函数
        self.std = std
        self.w = w
        self.x = x

    def fit(self, X, Y):
        self.x = X
        max_distance_list = []
        for i in range(X.shape[0]):
            max_distance_list.append(max([np.linalg.norm(m) for m in X - X[i]]))
        self.std = max(max_distance_list) / np.sqrt(2 * X.shape[0])
        # self.std = 0.1363
        list_result = []
        for i in range(X.shape[0]):
            if self.rbf.__name__ in str_no_s:
                list_result.append(self.rbf(X[i], X).ravel())
            else:
                list_result.append(self.rbf(X[i], X, self.std).ravel())
        Gaussian_result = np.array(list_result)
        # self.w = np.linalg.inv(Gaussian_result).dot(Y)
        self.w = np.linalg.solve(Gaussian_result, Y)
        return ','.join(map(str, self.w))

    def predict(self, X_Pre):
        list_pre_x = []
        for i in range(X_Pre.shape[0]):
            if self.rbf.__name__ in str_no_s:
                list_pre_x.append(self.rbf(X_Pre[i], self.x).ravel())
            else:
                list_pre_x.append(self.rbf(X_Pre[i], self.x, self.std).ravel())
        Y_Pre = np.array(list_pre_x).dot(self.w)
        return Y_Pre


if __name__ == "__main__":
    start = time.perf_counter()
    # d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])

    x_real = np.arange(-17, 18, 0.1)
    y_real = np.sin(x_real)

    x_train = np.arange(-17, 21, 3)
    y_train = np.sin(x_train)

    x_pred = np.arange(-17, 18, 0.1)

    rbf = RBF('gs')

    rbf.fit(x_train, y_train)

    y_pred = rbf.predict(x_pred)
    elapsed = (time.perf_counter() - start)

    # RR = 1 - (np.sum(np.square(data_pre[1] - y_Pre)) / np.sum(np.square(data_pre[1] - np.mean(data_pre[1]))))
    # print(RR)
    plt.plot(x_real, y_real, color='#ff0000', linestyle='-', label='real')
    plt.plot(x_pred, y_pred, color='#0000ff', linestyle=':', label='predict')
    plt.scatter(x_train, y_train, color='#000000', label='point', marker='s')
    # RR = 1 - (np.sum(np.square(y - y_Pre1)) / np.sum(np.square(y - np.mean(y))))
    # print(RR)
    plt.legend()
    plt.show()
    print("Time used:", elapsed)
