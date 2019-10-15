import numpy as np
import matplotlib.pyplot as plt


# def Gaussian(x, c, s):
#     return np.exp(-(x - c) ** 2 / (2 * s ** 2))


def Multiquadric(x, c, s):
    return np.sqrt((x - c) ** 2 + s ** 2)


def RBF(X, Y, X_Pre):
    list_Gaussian_result = []
    list_pre_x = []
    stds = (max(X) - min(X)) / len(X)
    for i in range(X.shape[0]):
        list_temp = []
        for j in range(X.shape[0]):
            list_temp.append(Multiquadric(X[i], X[j], stds))
        list_Gaussian_result.append(list_temp)
    Gaussian_result = np.array(list_Gaussian_result)
    w = np.linalg.inv(Gaussian_result).dot(Y)

    for i in range(X_Pre.shape[0]):
        list_temp = []
        for j in range(X.shape[0]):
            list_temp.append(Multiquadric(X_Pre[i], X[j], stds))
        list_pre_x.append(list_temp)
    Y_Pre = np.array(list_pre_x).dot(w)
    return Y_Pre


d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
y = np.array([22.3, 16.85, 11.4, 5.9501, 0.95417, 0.5, 0.95417, 5.9501, 11.4, 16.85, 22.3])
d_pred = np.arange(-17, 18)
Y_pre = RBF(d, y, d_pred)

print(Y_pre)
plt.plot(d, y, color='#ff0000', marker='+', linestyle='-',
         label='z-real')
plt.plot(d_pred, Y_pre, color='#0000ff', marker='+', linestyle='-.',
         label='z-predict')
plt.legend()
plt.show()
