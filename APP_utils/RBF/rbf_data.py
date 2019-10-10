import numpy as np
import matplotlib.pyplot as plt
from RBF import RBFNet
import time


def Text_Create(name, msg, hexOrfour):
    save_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/"
    if hexOrfour == 'four':
        save_path += 'post/'
    elif hexOrfour == 'hex':
        save_path += 'new_utils/post/'
    full_path = save_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


# from RBF_demo1 import RBFNet
#  coords.x,coords.y,coords.z
# 【输入str】：表面点的数据索引
# 【输出tuple】：返回tuple的第一个元素是x的坐标，第二个元素是y的坐标
# 【功能】：同一个点不同角度的坐标
def Get_Sample_Data(str):
    list_coords = str.split('\n')
    list_coords_slice = [listEle.split(',') for listEle in list_coords[0:len(list_coords)]]
    list_x = []
    list_y = []
    list_z = []
    list_coords_allFile = []
    for i in range(len(list_coords_slice)):
        list_coords_allFile.extend(list_coords_slice[i])
    for j in range(0, len(list_coords_slice[0]), 3):
        list_x_temp = []
        list_y_temp = []
        list_z_temp = []
        for h in range(j, len(list_coords_allFile), len(list_coords_slice[0])):
            list_x_temp.append(float(list_coords_allFile[h]))
            list_y_temp.append(float(list_coords_allFile[h + 1]))
            list_z_temp.append(float(list_coords_allFile[h + 2]))
        list_x.append(list_x_temp)
        list_y.append(list_y_temp)
        list_z.append(list_z_temp)
    return list_x, list_y, list_z


path_hex = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/RBF_test/post/"
path_coords = path_hex + "displacement_coords_surface_new.txt"
coordsFile = open(path_coords, "rt")
str_coords = coordsFile.read()
list_x, list_y, list_z = Get_Sample_Data(str_coords)


def realXYZ():
    # 预测值
    start = time.perf_counter()
    # x_len = len(list_x[0])
    y_len = len(list_y[0])
    z_len = len(list_z[0])
    d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    d_pred = np.arange(-17, 18)
    list_wb_y = []
    list_wb_z = []
    stds = ''
    # for i in range(len(list_y)):
    for i in range(3):
        # print(list_x[i][1:x_len])
        # print(list_y[i][1:y_len])
        # 取得list_x, list_y, list_z中每个元素不包含原始坐标值的数值
        # x_real1 = list_x[i][1:x_len]
        y_real1 = list_y[i][1:y_len]
        z_real1 = list_z[i][1:z_len]
        # 做为备份
        # x_real2 = x_real1.copy()
        y_real2 = y_real1.copy()
        z_real2 = z_real1.copy()
        # 对称
        # x_real1.reverse()
        y_real1.reverse()
        z_real1.reverse()
        # 组成没有中心的训练点
        # x_real = x_real1 + x_real2
        y_real = y_real1 + y_real2
        z_real = z_real1 + z_real2
        # 为训练点加上中心
        # x_real.insert(len(y_real2), list_x[i][0])
        y_real.insert(len(y_real2), list_y[i][0])
        z_real.insert(len(y_real2), list_z[i][0])

        # rbfnet_x = RBFNet()
        rbfnet_y = RBFNet()
        rbfnet_z = RBFNet()
        stds = str(rbfnet_y.stds)
        # w_x, b_x = rbfnet_x.fit(d, x_real)
        wb_y = rbfnet_y.fit(d, y_real)
        wb_z = rbfnet_z.fit(d, z_real)
        # x_pred = rbfnet_x.predict(d_pred)
        y_pred = rbfnet_y.predict(d_pred)
        z_pred = rbfnet_z.predict(d_pred)
        # plt.plot(d_pred, x_pred, color='#ff0000', marker='+', linestyle='-', label='x')
        plt.plot(d_pred, y_pred, color='#00ff00', marker='+', linestyle=':',
                 label=('' if i == 0 else '_') + 'y')
        plt.plot(d_pred, z_pred, color='#0000ff', marker='+', linestyle='-.',
                 label=('' if i == 0 else '_') + 'z')
        list_wb_y = np.concatenate((list_wb_y, wb_y))
        list_wb_z = np.concatenate((list_wb_z, wb_z))

        print("\r程序当前已完成：" + str(round(i / len(list_y) * 10000) / 100) + '%', end="")
    Text_Create('y_pre', ','.join(map(str, list_wb_y)) + ',' + stds, 'hex')
    Text_Create('z_pre', ','.join(map(str, list_wb_z)) + ',' + stds, 'hex')
    plt.legend()
    plt.tight_layout()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)


# def preCoord(list_x, list_y, list_z):

realXYZ()
# # 五点真实值
# print(list_x[0][1:len(list_x[0])])
# print(list_y[0][1:len(list_y[0])])
# y_real1 = list_x[0][1:len(list_x[0])]
# y_real2 = y_real1.copy()
# y_real1.reverse()
# y_real = y_real1 + y_real2
# y_real.insert(len(y_real2), list_x[0][0])
# # 全部真实值
# # stress
# # y_realAll_1 = [-6.9545229e-003, -2.7818092e-002, -4.1727141e-002, -6.2590707e-002,
# #                -8.3454281e-002, -0.10431784, -0.12518141, -0.14604498, -0.16690856,
# #                -0.18777213, -0.20863569, -0.22949927, -0.25036283, -0.27122641, -0.33381712,
# #                -0.31295353, -0.33381712]
# # x
# y_realAll_1 = [2.0859590516399997, 2.0859567106, 2.0859551497999997, 2.0859528088, 2.0859504677, 2.085948127,
#                2.085945786, 2.0859434439999998, 2.0859411029999997, 2.085938762, 2.085936421, 2.08593408, 2.085931739,
#                2.0859293979999998, 2.085922375, 2.085924716, 2.085922375]
# # y
# # y_realAll_1 = [0.95417, 2.3167, 3.225, 4.5876, 5.9501, 7.3126, 8.6751, 10.0377, 11.4, 12.763, 14.125, 15.488,
# #                16.85, 18.213, 22.3, 20.938, 22.3]
# # z
# # y_realAll_1 = [107.68564579999999, 107.66822479999999, 107.6566108, 107.6391898, 107.6217688, 107.6043478,
# #                107.5869228, 107.5695028, 107.5520828, 107.53466279999999, 107.51724279999999, 107.49982279999999,
# #                107.48240279999999, 107.46498279999999, 107.4127228, 107.4301428, 107.4127228]
# y_realAll_2 = y_realAll_1.copy()
# y_realAll_1.reverse()
# y_realAll = y_realAll_1 + y_realAll_2
# # y_realAll.insert(len(y_realAll_2), 0.5)
# # y_realAll.insert(len(y_realAll_2), 107.6914528)
# y_realAll.insert(len(y_realAll_2), 2.085959832)
#
#
#
# # plt.plot(X, y, '-o', label='true')
#
# # plt.plot(X, y_real, color='#fffff0', marker='1', label='real_Five')
#
# #
#
