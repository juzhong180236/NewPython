import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# result0 = np.random.randn(10000, 10000)
# result1 = np.random.randn(7000, 7000)
# result = np.linalg.inv(result1)
# print(result)


# str = [1, 2, 3]
#
# list_after = [val for val in str for i in range(2)]
#
# print(list_after)

# np.finfo(np.double)  # 浮点类型的机器限制
# print(np.finfo(np.double).bits)  # The number of bits occupied by the type.
# print(np.finfo(np.double).eps)
# print(np.finfo(np.double).epsneg)
# print(np.finfo(np.double).machar)
# print(np.finfo(np.double).machep)
# print(np.finfo(np.double).max)
# print(np.finfo(np.double).precision)
# print(np.finfo(np.double).tiny)
# print(np.zeros(0))

# test_array = np.arange(12).reshape(3, 4)
# test_array1 = np.arange(9).reshape(1, -1)
# print(test_array1)
# print(test_array.shape)
# x, y, z = np.atleast_2d(1, [1, 2], [[1, 2]])
# print(x, y)
# print(np.atleast_2d(test_array))
# print(np.atleast_2d(test_array1))
# print(test_array.reshape(-1, 1))

# Xc = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).reshape((-1, 2))
# yc = 0.5 * ((Xc * 6 - 2) ** 2) * np.sin((Xc * 6 - 2) * 2) + (Xc - 0.5) * 10. - 5
# x, y = np.atleast_2d(Xc, yc)
# print(x, y)
# print(x.shape)
# print(np.mean(x, axis=0))
# print(np.std(x, axis=0))

# degreeArr = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72]  # 0 8 16 24 32 40 48 56 64 72
# forceArr = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]  # 50 100 150 200 250 300 350 400 450 500
# combine = []
# for iDegree in range(len(degreeArr)):
#     for iForce in range(len(forceArr)):
#         combine.append((degreeArr[iDegree], forceArr[iForce]))
# fd = np.array(combine)
# print(fd)
# print(fd[1, 1])

# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_date:      2019/1/23
# file_name:        3DTest
# github            https://github.com/inspurer
# qq_mail           2391527690@qq.com

# -*- coding: utf-8 -*-
"""
绘制3d图形
"""
#
# import matplotlib.pyplot as plt
#
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np
#
# # 定义figure
# fig = plt.figure()
# # 创建3d图形的两种方式
# # 将figure变为3d
# ax = Axes3D(fig)
#
# # ax = fig.add_subplot(111, projection='3d')
#
# # 定义x, y
# x = np.arange(-4, 4, 0.25)
# y = np.arange(-5, 5, 0.25)
# # 生成网格数据
# X, Y = np.meshgrid(x, y)
# # 计算每个点对的长度
# R = np.sqrt(X ** 2 + Y ** 2)
# combine = []
# for _i in range(X.shape[0]):
#     for _j in range(X.shape[1]):
#         combine.append([X[_i, _j], Y[_i, _j]])
# _fd1 = np.array(combine)
# Z1 = np.sin(np.sqrt(_fd1[:, 0] ** 2 + _fd1[:, 1] ** 2)).reshape(40, 32)
# # print(_fd1[:, 0].reshape(32, 32))
# print(X)
# print(Y)
# # 计算Z轴的高度
# Z = np.sin(R)
# print(Z1)
# print(Z)
# 绘制3D曲面
# print(np.asarray([0, 500]).reshape(-1, 2))

# rstride:行之间的跨度  cstride:列之间的跨度
# rcount:设置间隔个数，默认50个，ccount:列的间隔个数  不能与上面两个参数同时出现

# train_samples_high = np.asarray([[50, 0], [50, 72], [200, 24], [350, 48], [500, 0], [500, 72]])
# stress = np.array([1, 2, 3, 4, 5, 6])
# fig = plt.figure()
# ax = Axes3D(fig)
# print(train_samples_high[:, 0])
# ax.scatter(
#     train_samples_high[:, 0],
#     train_samples_high[:, 1],
#     stress,
#     c='k',
# )
# plt.show()

# print(np.finfo(np.double).eps)
# _degreeArr = np.linspace(0, 72, 37)
# _forceArr = np.linspace(50, 500, 19)
# degree_arr_verification = np.arange(0, 74, 2)
# force_arr_verification = np.arange(50, 525, 25)
# print(_forceArr)
# print(_degreeArr)
# print(degree_arr_verification)
# print(force_arr_verification)
degree_arr_verification = np.arange(0, 74, 2, dtype=float)
degree_arr_verification = np.delete(degree_arr_verification, np.arange(4, 36, 4))
force_arr_verification = np.arange(50, 525, 25, dtype=float)
force_arr_verification = np.delete(force_arr_verification, np.arange(2, 18, 2))
# print(degree_arr_verification)
# print(force_arr_verification)
arr1 = np.arange(36).reshape(9, 4)
print(arr1)
print(arr1[np.array([1, 2, 6]),:])
