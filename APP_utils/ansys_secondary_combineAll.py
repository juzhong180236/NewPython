import os
import json


# 【程序介绍】变形
# 在一个文件夹下读取不同的位移文件数据，
# 然后将其添加到同一个txt文件中，每个位移文件的数据以换行符隔开

# 创建txt文件
def dict_To_jsonfile(name, dict):
    desktop_path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/post/"
    pathisExists = os.path.exists(desktop_path)
    # 判断结果
    if not pathisExists:
        # 如果不存在则创建目录
        os.makedirs(desktop_path)  # 创建目录操作函数
        print(desktop_path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(desktop_path + ' 目录已存在')
    full_path = desktop_path + name + '.json'  # 也可以创建一个.doc的word文档
    # 创建写入的文档
    file = open(full_path, 'w')
    json.dump(dict, file)
    file.close()


# 总的路径
path = "C:/Users/asus/Desktop/DT_RopewayDemo/APP_A_CantileverBeam/APP_models/list_new/post/"
path_dop_filename = path + "dop_noCoord.txt"  # 坐标数据文件名
path_stress_filename = path + "stress.txt"  # 应力数据文件名
path_dopSum_filename = path + "dop_Sum.txt"  # 总变形数据文件名
path_stressToColor_filename = path + "stress_To_Color_noStep.txt"  # 应力对应颜色值数据文件名
path_dopSumToColor_filename = path + "dopSum_To_Color_noStep.txt"  # 总变形对应颜色值数据文件名

arr_maxStress = []  # 存储应力差值最大的文件
# 读取dop文件数据
data_dop_file = open(path_dop_filename, 'rt')  # 以文本形式读取文件
data_dop_list = []  # 创建dop的列表，存储数据
data_dop_i = 0
for line in data_dop_file:  # 这些文件将ansys中的每一个静力学分析数据（比如施加位移2mm，4mm..各不同位移下的分析出的数据）都以换行符分割，所以line就是每一次分析的数据
    data_dop_list.append(line.split(','))
    dop_list = []
    for j in range(0, len(data_dop_list[data_dop_i]), 3):
        dop_list_temp = [data_dop_list[data_dop_i][j], data_dop_list[data_dop_i][j + 1],
                         data_dop_list[data_dop_i][j + 2]]
        dop_list.append(dop_list_temp)
    data_dop_list[data_dop_i] = dop_list
    data_dop_i += 1
print(len(data_dop_list))
# print(data_dop_list[0])
print("第一个文件读取完成!")

# 读取stress文件数据
data_stress_file = open(path_stress_filename, 'rt')  # 以文本形式读取文件
data_stress_list = []  # 创建dop的字典类型，存储数据
# data_stress_i = 0
for line in data_stress_file:  # 这些文件将ansys中的每一个静力学分析数据（比如施加位移2mm，4mm..各不同位移下的分析出的数据）都以换行符分割，所以line就是每一次分析的数据
    data_stress_list.append(line.split(','))
print(len(data_stress_list[0]))
# print(data_stress_list[0])
print("第二个文件读取完成!")

# 读取dop_Sum文件数据
data_dopSum_file = open(path_dopSum_filename, 'rt')  # 以文本形式读取文件
data_dopSum_list = []  # 创建dop的字典类型，存储数据
data_dopSum_i = 0
for line in data_dopSum_file:  # 这些文件将ansys中的每一个静力学分析数据（比如施加位移2mm，4mm..各不同位移下的分析出的数据）都以换行符分割，所以line就是每一次分析的数据
    data_dopSum_list.append(line.split(','))
print(len(data_dopSum_list[0]))
# print(data_dopSum_list[0])
print("第三个文件读取完成!")

# 读取stressToColor文件数据
data_stressToColor_file = open(path_stressToColor_filename, 'rt')  # 以文本形式读取文件
data_stressToColor_list = []  # 创建dop的列表，存储数据
data_stressToColor_i = 0
for line in data_stressToColor_file:  # 这些文件将ansys中的每一个静力学分析数据（比如施加位移2mm，4mm..各不同位移下的分析出的数据）都以换行符分割，所以line就是每一次分析的数据
    data_stressToColor_list.append(line.split(','))
    stressToColor_list = []
    for j in range(0, len(data_stressToColor_list[data_stressToColor_i]), 3):
        stressToColor_list_temp = [data_stressToColor_list[data_stressToColor_i][j],
                                   data_stressToColor_list[data_stressToColor_i][j + 1],
                                   data_stressToColor_list[data_stressToColor_i][j + 2]]
        stressToColor_list.append(stressToColor_list_temp)
    data_stressToColor_list[data_stressToColor_i] = stressToColor_list
    data_stressToColor_i += 1
print(len(data_stressToColor_list[0]))
print("第四个文件读取完成!")

# 读取dopSumToColor文件数据
data_dopSumToColor_file = open(path_dopSumToColor_filename, 'rt')  # 以文本形式读取文件
data_dopSumToColor_list = []  # 创建dop的列表，存储数据
data_dopSumToColor_i = 0
for line in data_dopSumToColor_file:  # 这些文件将ansys中的每一个静力学分析数据（比如施加位移2mm，4mm..各不同位移下的分析出的数据）都以换行符分割，所以line就是每一次分析的数据
    data_dopSumToColor_list.append(line.split(','))
    dopSumToColor_list = []
    for j in range(0, len(data_dopSumToColor_list[data_dopSumToColor_i]), 3):
        dopSumToColor_list_temp = [data_dopSumToColor_list[data_dopSumToColor_i][j],
                                   data_dopSumToColor_list[data_dopSumToColor_i][j + 1],
                                   data_dopSumToColor_list[data_dopSumToColor_i][j + 2]]
        dopSumToColor_list.append(dopSumToColor_list_temp)
    data_dopSumToColor_list[data_dopSumToColor_i] = dopSumToColor_list
    data_dopSumToColor_i += 1
print(len(data_dopSumToColor_list[0]))
print("第五个文件读取完成!")

data_combineAll_dict = {}  # 创建整合所有数据的字典，存储所有数据
iCount = len(data_dop_list)
jCount = len(data_dop_list[0])
for i in range(iCount):
    data_combineEach_dict = {}
    for j in range(jCount):
        # dop_dict = {"coordinates": data_dop_list[i][j]}  # 坐标数据
        # stress_dict = {"stress": data_stress_list[i][j]}  # 应力数据
        # stressToColor_dict = {"stressColor": data_stressToColor_list[i][j]}  # 应力颜色值数据
        # dopSum_dict = {"dopSum": data_dopSum_list[i][j]}  # 变形数据
        # dopSumtoColor_dict = {"dopSumColor": data_dopSumToColor_list[i][j]}  # 变形颜色值数据

        data_combineEach_dict[j] = {"coordinates": data_dop_list[i][j], "stress": data_stress_list[i][j],
                                    "stressColor": data_stressToColor_list[i][j], "dopSum": data_dopSum_list[i][j],
                                    "dopSumColor": data_dopSumToColor_list[i][j]}
    data_combineAll_dict[i] = data_combineEach_dict
    print("\rjson转化已完成：" + str(round(i / iCount * 100)) + '%', end="")
dict_To_jsonfile('combineAll', data_combineAll_dict)
