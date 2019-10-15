import numpy as np
import matplotlib.pyplot as plt
from RBF import RBFNet
import time


def Text_Create(name, msg, hexOrfour):
    save_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/"
    if hexOrfour == 'four':
        save_path += 'post/'
    elif hexOrfour == 'hex':
        save_path += 'RBF_net/post/'
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
def Get_Coords_Data(str):
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


def Get_Data(str, fileType):
    # 将多个文件（5个）合并过的变形、应力、坐标值数据等字符串以换行符分解为list
    list_separateByNewline = str.split('\n')
    # 将上述list的每一个str元素以逗号分解为list,用作计数
    # list_EachPart_Str2List = [listEle.split(',') for listEle in list_separateByNewline]
    list_EachPart_Str2List = list_separateByNewline[0].split(',')
    # 将所有数据放在一个list中
    list_allFile = ','.join(list_separateByNewline).split(',')
    # 获取
    if fileType == 'coords':
        list_x = []
        list_y = []
        list_z = []
        for j in range(0, len(list_EachPart_Str2List), 3):
            list_x_temp = []
            list_y_temp = []
            list_z_temp = []
            for h in range(j, len(list_allFile), len(list_EachPart_Str2List)):
                list_x_temp.append(float(list_allFile[h]))
                list_y_temp.append(float(list_allFile[h + 1]))
                list_z_temp.append(float(list_allFile[h + 2]))
            list_x.append(list_x_temp)
            list_y.append(list_y_temp)
            list_z.append(list_z_temp)
        return list_x, list_y, list_z
    elif fileType == 'stressOrdSum':
        list_stress = []
        for j in range(0, len(list_EachPart_Str2List)):
            list_stress_temp = []
            for h in range(j, len(list_allFile), len(list_EachPart_Str2List)):
                list_stress_temp.append(float(list_allFile[h]))
            list_stress.append(list_stress_temp)
        return list_stress


#
# def Get_Degree(list_input, i):
#     ss = list(map(lambda ele: ele[i], list_input))
#     print(min(ss))
#
#
# def Get_(list_input):
#     for i in range(len(list_input[0])):
#         Get_Degree(list_input, i)


path_hex = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/RBF_test/post/"

path_coords = path_hex + "displacement_coords_surface_new.txt"
path_allCoords = path_hex + "all.txt"
path_stress = path_hex + "e_stress_surface_new.txt"
path_allStress = path_hex + "all_stress.txt"
path_dSum = path_hex + "dSum_surface_new.txt"

coordsFile = open(path_coords, "rt")
allCoords = open(path_allCoords, "rt")
stress = open(path_stress, "rt")
allStress = open(path_allStress, "rt")
dSum = open(path_dSum, "rt")

str_coords = coordsFile.read()
# str_allCoords = allCoords.read()
str_Stress = stress.read()
# str_allStress = allStress.read()
str_dSum = dSum.read()

# 获取坐标点
list_x, list_y, list_z = Get_Data(str_coords, 'coords')
# list_xAll, list_yAll, list_zAll = Get_Data(str_allCoords, 'coords')
list_stress = Get_Data(str_Stress, 'stressOrdSum')
# list_stressAll = Get_Data(str_allStress, 'stressOrdSum')
list_dSum = Get_Data(str_dSum, 'stressOrdSum')


# Get_(list_x)
# Get_(list_y)
# Get_(list_z)


# 获取应力值
# stress = Get_Stress_Data()


def realXYZ():
    # 预测值
    start = time.perf_counter()
    d = np.array([-17, -13, -9, -5, -1, 0, 1, 5, 9, 13, 17])
    # d = np.array([0, 1, 5, 9, 13, 17])
    d_pred = np.arange(-17, 18)
    list_wb_y = []
    list_wb_z = []
    list_wb_stress = []
    list_wb_dSum = []
    stds = ''

    def Duplicated_list(list_input, dataType, i_count):
        if dataType == 'coords':
            xAll_real1 = list_input[i_count][1:]
            mean = list_input[i_count][0]
        elif dataType == 'stressOrdSum':
            xAll_real1 = list_input[i_count]
            mean = 0
        else:
            xAll_real1 = None
            mean = 0
        xAll_real2 = xAll_real1.copy()
        xAll_real1.reverse()
        xAll_real = xAll_real1 + xAll_real2
        xAll_real.insert(len(xAll_real2), mean)
        return xAll_real

    length = len(list_x)
    print(list_z[0])
    # for i in range(length):
    for i in range(1):
        # 取得list_x, list_y, list_z中每个元素不包含原始坐标值的数值
        y_real = Duplicated_list(list_y, 'coords', i)
        z_real = Duplicated_list(list_z, 'coords', i)
        stress_real = Duplicated_list(list_stress, 'stressOrdSum', i)
        dSum_real = Duplicated_list(list_dSum, 'stressOrdSum', i)
        # rbfnet_x = RBFNet()
        rbfnet_y = RBFNet()
        rbfnet_z = RBFNet()
        rbfnet_stress = RBFNet()
        rbfnet_dSum = RBFNet()
        # wb_v = rbfnet_x.fit(d, x_real)
        wb_y = rbfnet_y.fit(d, y_real)
        wb_z = rbfnet_z.fit(d, z_real)
        wb_stress = rbfnet_stress.fit(d, stress_real)
        wb_dSum = rbfnet_dSum.fit(d, dSum_real)
        # stds = str(rbfnet_y.stds)
        # x_pred = rbfnet_x.predict(d_pred)
        y_pred = rbfnet_y.predict(d_pred)
        z_pred = rbfnet_z.predict(d_pred)
        stress_pred = rbfnet_stress.predict(d_pred)
        dSum_pred = rbfnet_dSum.predict(d_pred)
        # plt.plot(d_pred, x_pred, color='#ff0000', marker='+', linestyle='-', label='x')
        # plt.plot(d_pred, y_pred, color='#00ff00', marker='+', linestyle=':',
        #          label=('' if i == 0 else '_') + 'y')
        zz = Duplicated_list(list_z, 'coords', i)
        plt.plot(d_pred, z_pred, color='#0000ff', marker='+', linestyle='-.',
                 label=('' if i == 0 else '_') + 'z-predict')
        plt.plot(d, zz, color='#ff00ff', marker='+', linestyle='-',
                 label=('' if i == 0 else '_') + 'z-real')
        # plt.plot(d_pred, stress_pred, color='#0000ff', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'stress')
        # plt.plot(d_pred, dSum_pred, color='#ff0000', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'dSum')
        # list_wb_y = np.concatenate((list_wb_y, wb_y))
        # list_wb_z = np.concatenate((list_wb_z, wb_z))
        list_wb_stress = np.concatenate((list_wb_stress, wb_stress))
        list_wb_dSum = np.concatenate((list_wb_dSum, wb_dSum))

        print("\r程序当前已完成：" + str(round(i / len(list_y) * 10000) / 100) + '%', end="")
    #
    # Text_Create('y_pre', ','.join(map(str, list_wb_y)) + ',' + stds, 'hex')
    # Text_Create('z_pre', ','.join(map(str, list_wb_z)), 'hex')
    # Text_Create('stress_pre', ','.join(map(str, list_wb_stress)), 'hex')
    # Text_Create('dSum_pre', ','.join(map(str, list_wb_dSum)), 'hex')

    # plt.plot(d_pred, Duplicated_list(list_zAll, 'coords'), color='#000000', marker='+', linestyle='-.')
    # plt.plot(d_pred, Duplicated_list(list_stressAll, 'stress'), color='#000000', marker='+', linestyle='-.')
    plt.legend()
    # plt.tight_layout()
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
