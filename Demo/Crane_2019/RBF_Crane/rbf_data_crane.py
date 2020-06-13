import numpy as np
import matplotlib.pyplot as plt
import time
from RBF_crane import RBF

path_switch = "/"
# 读取路径@@@@@@@@@@@@@@@@@@@@@(读mid)
path_hex = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "mid/"
'''调用RBF'''
rbf_type = 'lin_a'


def Text_Create(name, msg, hexOrfour):
    # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存post)
    save_path = "C:/Users/asus/Desktop/DT_Crane_Demo/APP_models" + path_switch + "post/"
    if hexOrfour == 'four':
        # 存储路径@@@@@@@@@@@@@@@@@@@@@@@(存post)
        # save_path += 'lin_a/'
        save_path = save_path
    elif hexOrfour == 'hex':
        save_path += 'lin_a/'
    full_path = save_path + name + '.txt'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()

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


path_coords = path_hex + "displacement_coords_surface_new.txt"
# path_allCoords = path_hex + "all.txt"
path_stress = path_hex + "e_stress_surface_new.txt"
# path_allStress = path_hex + "all_stress.txt"
path_dSum = path_hex + "dSum_surface_new.txt"

coordsFile = open(path_coords, "rt")
# allCoords = open(path_allCoords, "rt")
stress = open(path_stress, "rt")
# allStress = open(path_allStress, "rt")
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
    # 更换样本点时，这里要改
    d = np.array([0, 15, 30, 45, 60, 75])
    d_pred = np.arange(0, 75)
    list_w_y = []
    list_w_z = []
    list_w_stress = []
    list_w_dSum = []
    # list_w_y = ''
    # list_w_z = ''
    # list_w_stress = ''
    # list_w_dSum = ''
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
        xAll_real3 = xAll_real1.copy()
        xAll_real2.reverse()
        xAll_real = xAll_real2 + xAll_real3
        xAll_real.insert(len(xAll_real1), mean)
        return xAll_real

    length = len(list_x)
    i_max_x_y = 0
    for i in range(length):
        # for i in range(1):
        # 取得list_x, list_y, list_z中每个元素不包含原始坐标值的数值
        y_real = list_y[i]
        z_real = list_z[i]
        stress_real = list_stress[i]
        dSum_real = list_dSum[i]
        # rbfnet_x = RBFNet()
        rbfnet_y = RBF(rbf_type)
        rbfnet_z = RBF(rbf_type)
        rbfnet_stress = RBF(rbf_type)
        rbfnet_dSum = RBF(rbf_type)
        # wb_v = rbfnet_x.fit(d, x_real)
        w_y = rbfnet_y.fit(d, y_real)
        w_z = rbfnet_z.fit(d, z_real)
        w_stress = rbfnet_stress.fit(d, stress_real)
        w_dSum = rbfnet_dSum.fit(d, dSum_real)
        # 给出最高点处的点的轨迹
        # if int(max(y_real)) == 202 and i_max_x_y == 0 and int(min(map(abs, z_real))) == 0:
        #     print(w_y)
        #     print(w_z)
        #     max_w_y = w_y
        #     max_w_z = w_z
        #     i_max_x_y = 1
        stds = str(rbfnet_y.std)
        # x_pred = rbfnet_x.predict(d_pred)
        y_pred = rbfnet_y.predict(d_pred)
        z_pred = rbfnet_z.predict(d_pred)
        stress_pred = rbfnet_stress.predict(d_pred)
        dSum_pred = rbfnet_dSum.predict(d_pred)
        plt.plot(d_pred, y_pred, color='#0000ff', marker='+', linestyle='-.',
                 label=('' if i == 0 else '_') + 'y_predict')
        plt.plot(d, y_real, color='#ff00ff', marker='+', linestyle='-',
                 label=('' if i == 0 else '_') + 'y-real')
        # plt.plot(d_pred, z_pred, color='#ff0000', marker='+', linestyle='-.',
        #          label=('' if i == 0 else '_') + 'z-predict')
        # plt.plot(d_whole, z_real, color='#ff00ff', marker='+', linestyle='-.',
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
        list_w_y.append(w_y)
        list_w_z.append(w_z)
        list_w_stress.append(w_stress)
        list_w_dSum.append(w_dSum)

        print("\r程序当前已完成：" + str(round(i / len(list_y) * 10000) / 100) + '%', end="")
    #
    # Text_Create('y_pre', ','.join(map(str, list_w_y)) + ',' + stds, 'hex')
    # Text_Create('z_pre', ','.join(map(str, list_w_z)), 'hex')
    # Text_Create('stress_pre', ','.join(map(str, list_w_stress)), 'hex')
    # Text_Create('dSum_pre', ','.join(map(str, list_w_dSum)), 'hex')

    # 一般用这个
    Text_Create('y_pred_list', '\n'.join(list_w_y) + '\n' + stds + '\n' + ','.join(
        map(str, list(d))) + '\n' + rbf_type,
                'four')
    Text_Create('z_pred_list', '\n'.join(list_w_z) + '\n' + rbf_type, 'four')
    Text_Create('stress_pred_list', '\n'.join(list_w_stress) + '\n' + rbf_type, 'four')
    Text_Create('dSum_pred_list', '\n'.join(list_w_dSum) + '\n' + rbf_type, 'four')

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
    plt.legend()
    plt.tight_layout()
    plt.show()
    elapsed = (time.perf_counter() - start)
    print("Time used:", elapsed)


realXYZ()
