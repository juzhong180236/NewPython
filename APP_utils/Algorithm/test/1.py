import numpy as np
from threading import Thread
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.PRS import PRS


# from APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS import PRS


# a = [[1, 2, 5], [3, 4, 6]]
# print(type(1))
# b = [1, 2, 3, 4, 4, 5]
# print(list(map(lambda x: -x[1] if x[0] % 3 == 0 else x[1], enumerate(b))))

def fun(x1, y1, x2, y2, x):
    temp = (y2 - y1) / (x2 - x1)
    y = temp * (x - x1) + y1
    return y


# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073))
# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073 * 2))
# print(fun(0.06, 0.05, 0.28, 0.02543, 0.06 + 0.073 * 2 + 0.074))
#
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073))
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073 * 2))
# print(fun(0.06, 0, 0.28, 0.00943, 0.06 + 0.073 * 2 + 0.074))

# print(np.arctan(80 / 280) * 180 / np.pi)
# X_pre = np.array([3, 2])
# list_temp = []
# for i in range(X_pre.shape[0]):
#     _list_temp = []
#     for j in range(3 + 1):
#         _list_temp.append(X_pre[i] ** j)
#     list_temp.append(np.array(_list_temp))
# print(list_temp)
x_train = np.array([[3, 2], [2, 3], [4, 5]])
y_train = np.array([4, 5, 5])
p = PRS(name='simple_m')
print(p.prs)
print(p.fit(x_train, y_train))
print(p.predict(np.array([[3, 2]])))
a = np.array([1, 1, 3, 2, 9, 4])
b = [0.677844511177845, 0.6778445111778441, 0.8978144811478144, 1.187103770437104, -0.23014681348014693,
     -0.08800467133800473]
print(np.sum(a * b))
