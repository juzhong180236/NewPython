import numpy as np

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


# cmap是颜色映射表
# from matplotlib import cm
# ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap = cm.coolwarm)
# cmap = "rainbow" 亦可
# 我的理解的 改变cmap参数可以控制三维曲面的颜色组合, 一般我们见到的三维曲面就是 rainbow 的
# 你也可以修改 rainbow 为 coolwarm, 验证我的结论
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
# ax.plot_surface(X, Y, Z1, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))

# 绘制从3D曲面到底部的投影,zdir 可选 'z'|'x'|'y'| 分别表示投影到z,x,y平面
# zdir = 'z', offset = -2 表示投影到z = -2上
# ax.contour(X, Y, Z, zdir='z', offset=-2, cmap=plt.get_cmap('rainbow'))

# 设置z轴的维度，x,y类似
# ax.set_zlim(-2, 2)

# plt.show()

from collections import OrderedDict

""" 顔色 """
cmaps = OrderedDict()
cmaps['Miscellaneous'] = [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar']
print(cmaps.items())