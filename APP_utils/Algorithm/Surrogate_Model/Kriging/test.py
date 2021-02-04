import numpy as np


def gaussian_kernel(parameters, x1, x2):
    list_result = []
    if x1.shape[-1] != 1:
        for x1_ele in x1:
            list_result.append(np.exp(np.sum(-parameters * (x1_ele - x2) ** 2, axis=-1)).ravel())
    else:
        for x1_ele in x1:
            list_result.append(np.exp(-parameters * (x1_ele - x2) ** 2).ravel())
    return np.asarray(list_result)


def negative_log_likelihood_loss(parameters):
    pass


def gaussian(para_list, x1, x2):
    if x2.ndim != 1:
        return np.prod(np.exp(-para_list * (x1 - x2) ** 2), axis=-1)
    else:
        return np.exp(-para_list * (x1 - x2) ** 2)


def corelation(func, x, y, para_array):
    list_result = []
    for i in range(x.shape[0]):
        list_result.append(func(para_array, x[i], y).ravel())
    # print(np.array(list_result))
    return np.array(list_result)


def kernel(x1, x2):
    dist_matrix = np.sum(x1 ** 2, 1) + np.sum(x2 ** 2, 1) - 2 * np.dot(x1, x2.T)
    return np.exp(-0.5 / 2 ** 2 * dist_matrix)  # RBF核
    # return np.dot(x1, x2.T)


x_train = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]).reshape(-1, 2)

a = gaussian_kernel(0.3, x_train, x_train)
b = corelation(gaussian, x_train, x_train, 0.3)
print(a)
print(b)
print((a == b))
# aa = []
# for x1_ele in x_train:
#     print(x1_ele - x_train)
#     print(np.sum(x1_ele - x_train))
