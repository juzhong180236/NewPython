import numpy as np
import matplotlib.pyplot as plt
import os
import printf as pf
from RBF_crane import RBF
from PRS import PRS
from smt.applications import MFK

from scipy.interpolate import griddata


def ACC(x_real, x_predict):
    return 1 - np.sum(np.abs(x_real - x_predict) / x_real) / x_real.shape[-1]


def R2(x_real, x_predict):
    return 1 - (np.sum((x_predict - x_real) ** 2) / np.sum((x_real - np.mean(x_real)) ** 2))


#  coords.x,coords.y,coords.z
# 【输入str】：表面点的数据索引
# 【输出tuple】：
def get_Coords_Data(path_coord):
    textIO = open(path_coord, "rt")
    list_x = []
    list_y = []
    list_xy = []
    list_xy_predict = []
    i_line = 0
    for line in textIO:
        if i_line > 380:
            continue
        if i_line > 0:
            list_line = list(map(float, line.split('\t')))
            list_line.pop(0)
            list_xy.append([list_line[0], list_line[1]])
            list_xy_predict.append([list_line[0] + 11, list_line[1]])
            list_x.append(list_line[0])
            list_y.append(list_line[1])
        i_line += 1
    textIO.close()
    return np.array(list_x), np.array(list_y), np.array(list_xy), np.array(list_xy_predict)


def get_Stress_Data(path_stress):
    isExisted = os.path.exists(path_stress)
    if not isExisted:
        pf.printf(path_stress)
        pf.printf('上面列出的路径不存在，请设置正确路径！')
        return
    else:
        pf.printf('目录[' + path_stress + ']存在,正在读取...')
    files = os.listdir(path_stress)  # 获取当前文档下的文件
    list_stress_allfile = []  # 存放加上位移后的所有坐标值的list
    str_stress_allfile = ''
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            filename = os.path.basename(file)  # 返回文件名
            fullpath_input = path_stress + filename  # 得到文件夹中每个文件的完整路径
            textIO = open(fullpath_input, 'rt')  # 以文本形式读取文件
            list_stress = []
            i_line = 0
            for line in textIO:
                if i_line > 380:
                    continue
                if i_line > 0:
                    list_line = list(map(float, line.split('\t')))
                    list_line.pop(0)
                    list_stress.append(list_line[3])
                i_line += 1
            str_stress_eachfile = ','.join(map(str, list_stress))
            textIO.close()
            list_stress_allfile.append(np.array(list_stress))
            str_stress_allfile += str_stress_eachfile + '\n'
    return np.array(list_stress_allfile), str_stress_allfile.rstrip('\n')


# list_train_low = []
# for j in range(0, len(arr_stress_low_byfile[0])):
#     list_stress_temp = []
#     for h in range(0, len(arr_stress_low_byfile)):
#         print(j)
#         list_stress_temp.append(arr_stress_low_byfile[h][j])
#     list_train_low.append(list_stress_temp)
# print(list_train_low[1])
def get_Stress_Train_Data(string, fileType):
    # 将多个文件（5个）合并过的变形、应力、坐标值数据等字符串以换行符分解为list
    list_separateByNewline = string.split('\n')
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


# 读取路径@@@@@@@@@@@@@@@@@@@@@(读mid)
path_read = r"D:\Alai\data_Alai\points_400_20191218\data_single_displacement\\"

# 低保真数据
path_low_coord = path_read + r"low_train\30.txt"  # 坐标点路径
path_low_stress = path_read + r"low_train\\"  # 训练应力数据路径
arr_x_low, arr_y_low, arr_xy_low, arr_xy_predict_low = get_Coords_Data(path_low_coord)  # 坐标值数据
arr_stress_low_condition, str_stress_low_byfile = get_Stress_Data(path_low_stress)  # 每个状态不同节点的应力数据
arr_stress_low_node = get_Stress_Train_Data(str_stress_low_byfile, 'stressOrdSum')  # 每个节点不同状态的应力数据

# 高保真数据
path_high_coord = path_read + r"high_verify\45.txt"  # 坐标点路径
path_high_stress = path_read + r"high_verify\\"  # 验证应力数据路径
path_high_train = path_read + r"high_train\\"  # 验证应力数据路径
arr_x_high, arr_y_high, arr_xy_high, arr_xy_predict_high = get_Coords_Data(path_high_coord)  # 坐标值数据
arr_stress_high, str_stress_high = get_Stress_Data(path_high_stress)  # 每个状态不同节点的应力数据
arr_stress_high_train, str_stress_high_train = get_Stress_Data(path_high_train)  # 每个状态不同节点的应力数据


def low_predict_data_by_force():
    d_train_low = np.array([30, 60, 90])
    d_predict_low = np.array([45, 75])
    # stds = ''
    # 每个节点不同状态的预测值
    list_preddict_node = []
    length = len(arr_stress_low_node)
    for i in range(length):
        stress_real = np.array(arr_stress_low_node[i])
        rbfnet_stress = RBF('mq')
        w_stress = rbfnet_stress.fit(d_train_low, stress_real)
        stress_predict = rbfnet_stress.predict(d_predict_low)
        list_preddict_node.append(stress_predict)
        # print("\r程序当前已完成：" + str(round((i + 1) / length * 10000) / 100) + '%', end="")
    # 每个状态不同节点的预测值
    list_stress_condition = []
    for i in range(0, len(list_preddict_node[0])):
        list_stress_temp = []
        for j in range(0, len(list_preddict_node)):
            list_stress_temp.append(list_preddict_node[j][i])
        list_stress_condition.append(list_stress_temp)
    return list_stress_condition, list_preddict_node

    # arr_train = np.array(arr_stress_low_train)
    # arr_stress_low_predict_1 = np.array(list_pred_1).flatten()
    # arr_stress_low_predict_2 = np.array(list_pred_2).flatten()
    # arr_stress_low_predict_3 = np.array(list_pred_3).flatten()
    # arr_stress_low_predict_4 = np.array(list_pred_4).flatten()


predict, predict_node = low_predict_data_by_force()
list_RR_rbf = []
# print(np.array(list_preddict_condition_prs)[0][0])
# print(len(arr_stress_high))
for i in range(2):
    RR = 1 - (np.sum((np.array(predict)[i] - arr_stress_high[i]) ** 2) / np.sum(
        (arr_stress_high[i] - np.mean(arr_stress_high[i])) ** 2))
    list_RR_rbf.append(format(RR, '.4f'))
print('rbf低保真r2' + str(list_RR_rbf))

list_acc_low = []
for i in range(2):
    acc = ACC(arr_stress_high[i], np.array(predict)[i])
    list_acc_low.append(format(acc, '.4f'))
print('rbf低保真acc' + str(list_acc_low))


def high_predict_data_by_force():
    d_train = arr_xy_low
    d_predict = arr_xy_high
    list_y = []
    yt_c = np.array(low_predict_data_by_force()[0])
    for i in range(4):
        list_y.append(yt_c[i])
    # stds = ''
    list_preddict_condition_prs = []
    for i in range(4):
        prs = PRS(name='zi', m=3)
        w_stress = prs.fit(d_train, list_y[i])
        prs_predict = prs.predict(d_predict)
        list_preddict_condition_prs.append(prs_predict)
    list_RR_prs = []
    # print(np.array(list_preddict_condition_prs)[0][0])
    # print(len(arr_stress_high))
    for i in range(4):
        RR = 1 - (np.sum((np.array(list_preddict_condition_prs)[i] - arr_stress_high[i]) ** 2) / np.sum(
            (arr_stress_high[i] - np.mean(arr_stress_high[i])) ** 2))
        list_RR_prs.append(RR)
    print(list_RR_prs)
    # 每个状态不同节点的预测值
    list_preddict_condition = []
    for i in range(4):
        rbfnet_stress = RBF('mq')
        w_stress = rbfnet_stress.fit(d_train, list_y[i])
        stress_predict = rbfnet_stress.predict(d_predict)
        list_preddict_condition.append(stress_predict)
        # print("\r程序当前已完成：" + str(round((i + 1) / 4 * 10000) / 100) + '%', end="")
    # 每个状态不同节点的预测值
    # list_stress_condition = []
    # for i in range(0, len(list_preddict_condition[0])):
    #     list_stress_temp = []
    #     for j in range(0, len(list_preddict_condition)):
    #         list_stress_temp.append(list_preddict_condition[j][i])
    #     list_stress_condition.append(list_stress_temp)
    list_RR = []
    # print(np.array(list_preddict_condition)[0][0])
    # print(len(arr_stress_high))
    for i in range(4):
        RR = 1 - (np.sum((np.array(list_preddict_condition)[i] - arr_stress_high[i]) ** 2) / np.sum(
            (arr_stress_high[i] - np.mean(arr_stress_high[i])) ** 2))
        list_RR.append(RR)
    print(list_RR)
    return np.array(list_preddict_condition)


def cokriging(i):
    # Xt_e = np.array([[1.57894737, 17.8947368],
    #                  [8.42105263, 17.8947368],
    #                  [1.57894737, 2.10526316],
    #                  [8.42105263, 2.10526316],
    #                  ])
    Xt_e = np.array([[50.0891841, 11.000994],
                     [49.9108168, 38.999006],
                     [84.200043, 41.5655806],
                     [16.0943345, 7.97111717],
                     [15.7955774, 41.584603],
                     [83.9713379, 7.94023456],
                     ])
    Xt_c = arr_xy_low

    yt_e = arr_stress_high_train[i]
    yt_c = np.array(low_predict_data_by_force()[0][i])

    sm = MFK(theta0=np.array(Xt_e.shape[1] * [1.0]), print_global=False)
    sm.set_training_values(Xt_c, yt_c, name=0)
    sm.set_training_values(Xt_e, yt_e)
    sm.train()

    Xp = arr_xy_high
    y = sm.predict_values(Xp)
    # MSE = sm.predict_variances(Xp)
    # der = sm.predict_derivatives(Xp, kx=0)
    return y.flatten()


def draw():
    # 低保真图像(仿真真实值)
    # arr_verify_1 = arr_stress_low_condition[0]
    # arr_verify_2 = arr_stress_low_condition[1]
    # arr_verify_3 = arr_stress_low_condition[2]
    # arr_verify_4 = arr_stress_low_condition[3]
    # arr_verify_5 = arr_stress_low_condition[4]
    # 高保真图像(仿真真实值)
    arr_verify_1 = arr_stress_high[0]
    arr_verify_2 = arr_stress_high[1]
    # arr_verify_3 = arr_stress_high[2]
    # arr_verify_4 = arr_stress_high[3]
    # 高保真图像(cokriging坐标预测值)
    arr_predict_1 = cokriging(0)
    arr_predict_2 = cokriging(1)
    # arr_predict_3 = cokriging(2)
    # arr_predict_4 = cokriging(3)
    arr_predict = [arr_predict_1, arr_predict_2]
    # arr_predict = [arr_predict_1, arr_predict_2, arr_predict_3, arr_predict_4]
    # 高保真图像(rbf力与角度预测值)
    arr_predict_rbf_1 = np.array(low_predict_data_by_force()[0][0])
    arr_predict_rbf_2 = np.array(low_predict_data_by_force()[0][1])
    # arr_predict_rbf_3 = np.array(low_predict_data_by_force()[0][2])
    # arr_predict_rbf_4 = np.array(low_predict_data_by_force()[0][3])

    list_RR = []
    for i in range(2):
        RR = 1 - (np.sum((arr_predict[i] - arr_stress_high[i]) ** 2) / np.sum(
            (arr_stress_high[i] - np.mean(arr_stress_high[i])) ** 2))
        list_RR.append(format(RR, '.4f'))
    print('co-kriging变保真r2' + str(list_RR))
    list_acc_high = []
    for i in range(2):
        acc_high = ACC(arr_stress_high[i], np.array(arr_predict)[i])
        list_acc_high.append(format(acc_high, '.4f'))
    print('co-kriging变保真acc' + str(list_acc_high))
    # plt.figure()
    #
    # fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(20, 40))
    #
    # cha_1 = 1 - np.abs((arr_verify_1 - arr_predict_1) / arr_verify_1)
    # cha_2 = 1 - np.abs((arr_verify_2 - arr_predict_2) / arr_verify_2)
    # cha_3 = 1 - np.abs((arr_verify_3 - arr_predict_3) / arr_verify_3)
    # cha_4 = 1 - np.abs((arr_verify_4 - arr_predict_4) / arr_verify_4)
    # # cha_1 = ACC(arr_verify_1, arr_predict_1)
    # # cha_2 = ACC(arr_verify_2, arr_predict_2)
    # # cha_3 = ACC(arr_verify_3, arr_predict_3)
    # # cha_4 = ACC(arr_verify_4, arr_predict_4)
    # r_1 = R2(arr_verify_1, arr_predict_1)
    # r_2 = R2(arr_verify_2, arr_predict_2)
    # r_3 = R2(arr_verify_3, arr_predict_3)
    # r_4 = R2(arr_verify_4, arr_predict_4)
    # # draw_xy_list = [[arr_verify_1, arr_predict_1], cha_1,
    # #                 [arr_verify_2, arr_predict_2], cha_2,
    # #                 [arr_verify_3, arr_predict_3], cha_3,
    # #                 [arr_verify_4, arr_predict_4], cha_4,
    # #                 ]
    # draw_xy_list = [arr_verify_1, arr_predict_1, cha_1,
    #                 arr_verify_2, arr_predict_2, cha_2,
    #                 arr_verify_3, arr_predict_3, cha_3,
    #                 arr_verify_4, arr_predict_4, cha_4]
    # # 高保真仿真真实数据的XY面坐标范围（即放在图中的哪个位置）
    # X = np.linspace(min(arr_x_high) - 1, max(arr_x_high) + 1, 100)
    # Y = np.linspace(min(arr_y_high) - 1, max(arr_y_high) + 1, 100)
    # # 高保真预测数据的XY面坐标范围（即相对上面的位置往又移动11）
    # X_predict = np.array(list(map(lambda x: x + 11, X)))
    # # 将上述两组数据广播为100*100的一个面信息
    # grid_X, grid_Y = np.meshgrid(X, Y)
    # grid_X_predict, grid_Y_predict = np.meshgrid(X_predict, Y)
    # title = np.array(['45-30', '60-15', '60-45', '75-30']).repeat(3)
    # for ax, draw_xy, i, t, in zip(axs.flat, draw_xy_list, range(len(draw_xy_list)), title):
    #     if (i + 1) % 3 == 0:
    #         data = griddata(arr_xy_high, draw_xy, xi=(grid_X, grid_Y), method='cubic')
    #         ax_subplt = ax.contourf(grid_X, grid_Y, data, levels=100, cmap='jet')
    #         fig.colorbar(ax_subplt, ax=ax)
    #         ax.set_title('1-|(real-predict)/real| ' + t)
    #     else:
    #         # method=nearest/linear/cubic 将数据变为插值
    #         data = griddata(arr_xy_high, draw_xy, xi=(grid_X, grid_Y), method='cubic')
    #         # data2 = griddata(arr_xy_predict_high, draw_xy[1], xi=(grid_X_predict, grid_Y_predict), method='cubic')
    #         ax_subplt = ax.contourf(grid_X, grid_Y, data, levels=100, cmap='jet')
    #         # ax_subplt2 = ax.contourf(grid_X_predict, grid_Y_predict, data2, levels=100, cmap='jet')
    #         ax.set_title(t)
    #         fig.colorbar(ax_subplt, ax=ax)
    #         # fig.colorbar(ax_subplt2, ax=ax)
    #
    # # nn1 = np.array(list_RR)
    # # plt.figure()
    # # print(max(nn1))
    # # print(min(nn1))
    # # fig, axs2 = plt.subplots(nrows=1, ncols=1, figsize=(20, 20))
    # # zzr = griddata(arr_xy, nn1, xi=(grid_X, grid_Y), method='cubic')
    # # ax_subplt = axs2.contourf(grid_X, grid_Y, zzr, levels=100, cmap='jet')
    # # fig.colorbar(ax_subplt, ax=axs2)
    # # axs2.set_title('r2')
    #
    # # plt.legend()
    # plt.tight_layout()
    # plt.show()


draw()
