import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


def half_circle(x):
    """
    原心：(1,0),半径为1
    半圆函数：(x-1)^2+y^2 = 1
    """
    return 0.1 + np.exp(-x ** 2 / (2 * 0.25))


"""
梯形法求积分：半圆线和x轴包围的面积
"""
N = 10000
x = np.linspace(-2, 2, num=N)  # ,endpoint=True)
print(x)
dh = 4 / N
y = half_circle(x)
"""
梯形法求积分：（上底+ 下底）*高/2
"""
S = sum((y[1:] + y[:-1]) * dh / 2)

print("=========%s==========" % "梯形法")
print("面积：%f" % S)

"""
直接调用intergrate的积分函数quad
"""
S2, err = integrate.quad(half_circle, -2, 2)
S3, err1 = integrate.quad(half_circle, -1.5, 1.5)
print(S3/S2)
print("=========%s==========" % "quad")
print("面积：%f" % S2)

"""
多重定积分:注意积分顺序
"""

# def half_sphere(y, x):
#     """
#     球心：（1，0，0）
#     半径：1
#     半球：(x-1)^2+y^2+z^2=1
#     """
#     return (1 - (x - 1) ** 2 - y ** 2) ** 0.5
#
#
# """
# 积分顺序：
# v = V x in [0,2] :V y in [-g(x),h(x)]
# """
# V3, err = integrate.dblquad(half_sphere, 0, 2, lambda x: -half_circle(x), lambda x: half_circle(x))
# print("========%s===========" % "dblquad")
# print("体积：%f" % V3)
plt.plot(x, y, color='#ff0000', marker='+', linestyle='-',
         label='z-real')
# plt.plot(d_pred, y_Pre1, color='#0000ff', marker='+', linestyle='-.',
#          label='z-predict')
# RR = 1 - (np.sum(np.square(y - y_Pre1)) / np.sum(np.square(y - np.mean(y))))
# print(RR)
plt.legend()
plt.show()
