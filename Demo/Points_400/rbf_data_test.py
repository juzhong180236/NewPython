import numpy as np
import matplotlib.pyplot as plt
import time
from RBF_crane import RBF
from scipy.interpolate import griddata

# 读取路径@@@@@@@@@@@@@@@@@@@@@(读mid)
path_hex = r"C:\Users\asus\Desktop\History\History_codes\points_400\test\\"
'''调用哪种rbf'''
rbf_type = {'y': 'lin_a', 'z': 'lin_a', 'stress': 'mq', 'dSum': 'lin_a'}


def Text_Create(name, msg, hexOrfour):
    # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存post)
    save_path = "C:/Users/asus/Desktop/test/"
    if hexOrfour == 'four':
        # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存post)
        save_path += 'lin_a/'
    elif hexOrfour == 'hex':
        save_path += 'RBF_Surrogate_pillar/'
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
    list_coords = str.split(',')

    # list_coords_slice = [listEle.split(',') for listEle in list_coords[0:len(list_coords)]]
    list_x = []
    list_y = []
    list_xy = []
    for i in range(0, len(list_coords), 3):
        list_xy.append([float(list_coords[i]), float(list_coords[i + 1])])
        list_x.append(float(list_coords[i]))
        list_y.append(float(list_coords[i + 1]))

    # list_z = []
    # list_coords_allFile = []
    # for i in range(len(list_coords_slice)):
    #     list_coords_allFile.extend(list_coords_slice[i])
    # for j in range(0, len(list_coords_slice[0]), 3):
    #     list_x_temp = []
    #     list_y_temp = []
    #     list_z_temp = []
    #     for h in range(j, len(list_coords_allFile), len(list_coords_slice[0])):
    #         list_x_temp.append(float(list_coords_allFile[h]))
    #         list_y_temp.append(float(list_coords_allFile[h + 1]))
    #         list_z_temp.append(float(list_coords_allFile[h + 2]))
    #     list_x.append(list_x_temp)
    #     list_y.append(list_y_temp)
    #     list_z.append(list_z_temp)
    return np.array(list_x), np.array(list_y), np.array(list_xy)


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


path_coords = path_hex + "coords_result.txt"
# path_allCoords = path_hex + "all.txt"
path_stress = path_hex + "stress.txt"
# path_allStress = path_hex + "all_stress.txt"
path_dSum = path_hex + "dSum_surface_new.txt"
path_stress_test = path_hex + "stress_test.txt"

coordsFile = open(path_coords, "rt")
# allCoords = open(path_allCoords, "rt")

stress = open(path_stress, "rt")
stress_test = open(path_stress_test, "rt")

# allStress = open(path_allStress, "rt")
# dSum = open(path_dSum, "rt")

str_coords = coordsFile.read()
# str_allCoords = allCoords.read()
str_Stress = stress.read()
str_Stress_test = stress_test.read()
list_train_1 = list(map(float, (str_Stress_test.split('\n'))[0].split(',')))
list_train_2 = list(map(float, (str_Stress_test.split('\n'))[1].split(',')))
list_train_3 = list(map(float, (str_Stress_test.split('\n'))[2].split(',')))
list_train_4 = list(map(float, (str_Stress_test.split('\n'))[3].split(',')))
list_train = []
for i in range(len(list_train_1)):
    list_train.append([list_train_1[i], list_train_2[i], list_train_3[i], list_train_4[i]])
# str_allStress = allStress.read()
# str_dSum = dSum.read()

# 获取坐标点
arr_x, arr_y, arr_xy = Get_Coords_Data(str_coords)
# list_xAll, list_yAll, list_zAll = Get_Data(str_allCoords, 'coords')
list_stress = Get_Data(str_Stress, 'stressOrdSum')
list_stress_test = Get_Data(str_Stress_test, 'stressOrdSum')


# list_stressAll = Get_Data(str_allStress, 'stressOrdSum')
# list_dSum = Get_Data(str_dSum, 'stressOrdSum')


# Get_(list_x)
# Get_(list_y)
# Get_(list_z)


# 获取应力值
# stress = Get_Stress_Data()


def realXYZ():
    # 预测值
    start = time.perf_counter()
    # 更换样本点时，这里要改
    # d = np.array([-30, -22, -13, -5, 0, 5, 13, 22, 30])
    forceArr = [10, 20, 30]
    degreeArr = [30, 45, 60]
    combine = []
    for iForce in range(len(forceArr)):
        for iDegree in range(len(degreeArr)):
            combine.append((forceArr[iForce], degreeArr[iDegree]))
    d = np.array(combine)
    d_pred_1 = np.array([[15, 37.5]])
    d_pred_2 = np.array([[15, 52.5]])
    d_pred_3 = np.array([[25, 37.5]])
    d_pred_4 = np.array([[25, 52.5]])
    # list_w_y = []
    # list_w_z = []
    list_w_stress = []
    # list_w_dSum = []
    # list_w_y = ''
    # list_w_z = ''
    # list_w_stress = ''
    # list_w_dSum = ''
    # stds = ''
    list_pred = []
    list_pred_1 = []
    list_pred_2 = []
    list_pred_3 = []
    list_pred_4 = []
    length = len(list_stress)
    for i in range(length):
        # for i in range(1):
        # 取得list_x, list_y, list_z中每个元素不包含原始坐标值的数值
        # y_real = list_y
        # z_real = list_z
        stress_real = list_stress[i]
        # dSum_real = list_dSum
        # rbfnet_x = RBFNet()
        # rbfnet_y = RBF(rbf_type['y'])
        # rbfnet_z = RBF(rbf_type['z'])
        rbfnet_stress = RBF(rbf_type['stress'])
        # rbfnet_dSum = RBF(rbf_type['dSum'])
        # wb_v = rbfnet_x.fit(d, x_real)
        # w_y = rbfnet_y.fit(d, y_real)
        # w_z = rbfnet_z.fit(d, z_real)
        w_stress = rbfnet_stress.fit(d, stress_real)
        # w_dSum = rbfnet_dSum.fit(d, dSum_real)
        # stds = str(rbfnet_y.std)
        # x_pred = rbfnet_x.predict(d_pred)
        # y_pred = rbfnet_y.predict(d_pred)
        # z_pred = rbfnet_z.predict(d_pred)
        stress_pred_1 = rbfnet_stress.predict(d_pred_1)
        stress_pred_2 = rbfnet_stress.predict(d_pred_2)
        stress_pred_3 = rbfnet_stress.predict(d_pred_3)
        stress_pred_4 = rbfnet_stress.predict(d_pred_4)
        list_pred.append([stress_pred_1[0], stress_pred_2[0], stress_pred_3[0], stress_pred_4[0]])
        list_pred_1.append(stress_pred_1)
        list_pred_2.append(stress_pred_2)
        list_pred_3.append(stress_pred_3)
        list_pred_4.append(stress_pred_4)
        # list_RR.append(RR)
        # dSum_pred = rbfnet_dSum.predict(d_pred)
        # plt.plot(d_pred, y_pred, color='#0000ff', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'y_predict')
        # plt.plot(d, y_real, color='#ff00ff', marker='+', linestyle='-',
        #          label=('' if i == 0 else '_') + 'y-real')
        # plt.plot(d_pred, z_pred, color='#ff0000', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'z-predict')
        # plt.plot(d, z_real, color='#0000ff', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'stress_predict')
        # plt.plot(d_pred, dSum_pred, color='#ffff00', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'dSum_predict')
        # plt.plot(d, dSum_real, color='#455500', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'dSum_predict')
        # plt.plot(d_pred, stress_pred, color='#ffff00', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'dSum_predict')
        # plt.plot(d, stress_real, color='#455500', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'dSum_predict')
        # list_w_y = np.concatenate((list_w_y, w_y))
        # list_w_z = np.concatenate((list_w_z, w_z))
        # list_w_stress = np.concatenate((list_w_stress, w_stress))
        # list_w_dSum = np.concatenate((list_w_dSum, w_dSum))
        # list_w_y += w_y + '\n'
        # list_w_z += w_z + '\n'
        # list_w_stress += w_stress + '\n'
        # list_w_dSum += w_dSum + '\n'
        # list_w_y.append(w_y)
        # list_w_z.append(w_z)
        list_w_stress.append(w_stress)
        # list_w_dSum.append(w_dSum)

        print("\r程序当前已完成：" + str(round(i / len(list_stress) * 10000) / 100) + '%', end="")
    arr_train_1 = np.array(list_train_1)
    arr_train_2 = np.array(list_train_2)
    arr_train_3 = np.array(list_train_3)
    arr_train_4 = np.array(list_train_4)
    arr_train = np.array(list_train)
    arr_pred_1 = np.array(list_pred_1).flatten()
    arr_pred_2 = np.array(list_pred_2).flatten()
    arr_pred_3 = np.array(list_pred_3).flatten()
    arr_pred_4 = np.array(list_pred_4).flatten()
    arr_pred = np.array(list_pred)
    dd = np.arange(1, 401)
    list_RR = []
    for i in range(arr_train.shape[0]):
        RR = 1 - (np.sum(np.square(arr_pred[i] - arr_train[i])) / np.sum(
            np.square(arr_pred[i] - np.mean(arr_pred[i]))))
        list_RR.append(RR)
    plt.figure()
    fig, axs = plt.subplots(nrows=7, ncols=2, figsize=(10, 30))
    zz = arr_train_1
    zz1 = arr_train_2
    zz2 = arr_train_3
    zz3 = arr_train_4
    zz4 = arr_pred_1
    zz5 = arr_pred_2
    zz6 = arr_pred_3
    zz7 = arr_pred_4
    cha_1 = (arr_train_1 - arr_pred_1) / arr_train_1
    cha_2 = (arr_train_2 - arr_pred_2) / arr_train_2
    cha_3 = (arr_train_3 - arr_pred_3) / arr_train_3
    cha_4 = (arr_train_4 - arr_pred_4) / arr_train_4
    nn1 = np.array(list_RR)
    zz_list = [zz, zz4, zz1, zz5, zz2, zz6, zz3, zz7, cha_1, cha_2, cha_3, cha_4, nn1]
    zz_list_1 = []

    # print(min(arr_x), max(arr_x))
    # print(min(arr_y), max(arr_y))

    X = np.linspace(min(arr_x), max(arr_x), 100)
    Y = np.linspace(min(arr_y), max(arr_y), 100)
    #
    # print(arr_xy.shape)
    # 广播为100*100的一个面信息
    grid_X, grid_Y = np.meshgrid(X, Y)
    for ax, z in zip(axs.flat, zz_list):
        # method=nearest/linear/cubic 将数据变为插值
        zz = griddata(arr_xy, z, xi=(grid_X, grid_Y), method='cubic')
        ax.contourf(grid_X, grid_Y, zz, levels=20, cmap='jet')
        # plt.contourf(zz1)

    # zz = np.mat(zz)
    # zz, zz1 = np.meshgrid(arr_train_1, arr_train_1)
    # xx, xx1 = np.meshgrid(arr_x, arr_x)
    # yy, yy = np.meshgrid(arr_y, arr_y)
    # print(xx.shape)

    # plt.figure()
    # plt.plot(dd, np.array(list_RR), color='#ff0000', linestyle='-', linewidth=0.5,
    #          label='z-real')
    # plt.title('R2')
    # plt.figure()
    # plt.plot(dd, arr_pred_1, color='#ff0000', linestyle='--', linewidth=0.5,
    #          label='stress_predict')
    # plt.plot(dd, arr_train_1, color='#0000ff', linestyle='-', linewidth=0.5,
    #          label='stress_real')
    # plt.title('force=' + str(d_pred_1[0][0]) + '    degree=' + str(d_pred_1[0][1]))
    # plt.figure()
    # plt.plot(dd, arr_pred_2, color='#ff0000', linestyle='--', linewidth=0.5,
    #          label='stress_predict')
    # plt.plot(dd, arr_train_2, color='#0000ff', linestyle='-', linewidth=0.5,
    #          label='stress_real')
    # plt.title('force=' + str(d_pred_2[0][0]) + '    degree=' + str(d_pred_2[0][1]))
    # plt.figure()
    # plt.plot(dd, arr_pred_3, color='#ff0000', linestyle='--', linewidth=0.5,
    #          label='stress_predict')
    # plt.plot(dd, arr_train_3, color='#0000ff', linestyle='-', linewidth=0.5,
    #          label='stress_real')
    # plt.title('force=' + str(d_pred_3[0][0]) + '    degree=' + str(d_pred_3[0][1]))
    # plt.figure()
    # plt.plot(dd, arr_pred_4, color='#ff0000', linestyle='--', linewidth=0.5,
    #          label='stress_predict')
    # plt.plot(dd, arr_train_4, color='#0000ff', linestyle='-', linewidth=0.5,
    #          label='stress_real')
    # plt.title('force=' + str(d_pred_4[0][0]) + '    degree=' + str(d_pred_4[0][1]))
    # plt.legend()
    # plt.show()
    # Text_Create('y_pre', ','.join(map(str, list_w_y)) + ',' + stds, 'hex')
    # Text_Create('z_pre', ','.join(map(str, list_w_z)), 'hex')
    # Text_Create('stress_pre', ','.join(map(str, list_w_stress)), 'hex')
    # Text_Create('dSum_pre', ','.join(map(str, list_w_dSum)), 'hex')
    # print('\n'.join(list_w_y) + '\n' + stds + '\n' + ','.join(map(str, list(d))) + '\n' + rbf_type['y'])
    # 一般用这个
    # Text_Create('y_pred_list', '\n'.join(list_w_y), 'four')
    # Text_Create('y_pred_list',
    #             '\n'.join(list_w_y) + '\n' + stds + '\n' + ','.join(map(str, list(d))) + '\n' + rbf_type['y'],
    #             'four')
    # Text_Create('z_pred_list', '\n'.join(list_w_z) + '\n' + rbf_type['z'], 'four')
    # Text_Create('stress_pred_list', '\n'.join(list_w_stress) + '\n' + rbf_type['stress'], 'four')
    # Text_Create('dSum_pred_list', '\n'.join(list_w_dSum) + '\n' + rbf_type['dSum'], 'four')

    # Text_Create('y_pred_list', '\n'.join(list_w_y) + '\n' + stds, 'hex')
    # Text_Create('z_pred_list', '\n'.join(list_w_z), 'hex')
    # Text_Create('stress_pred_list', '\n'.join(list_w_stress), 'hex')
    # Text_Create('dSum_pred_list', '\n'.join(list_w_dSum), 'hex')

    # Text_Create('y_pre_str', list_w_y + stds, 'hex')
    # Text_Create('z_pre_str', list_w_z.rstrip('\n'), 'hex')
    # Text_Create('stress_pre_str', list_w_stress.rstrip('\n'), 'hex')
    # Text_Create('dSum_pre_str', list_w_dSum.rstrip('\n'), 'hex')
    # plt.plot(d_pred, Duplicated_list(list_zAll, 'coords'), color='#000000', marker='+', linestyle='-.')
    # plt.plot(d_pred, Duplicated_list(list_stressAll, 'stress'), color='#000000', marker='+', linestyle='-.')
    # plt.legend()
    plt.tight_layout()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)


realXYZ()
