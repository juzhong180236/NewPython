import numpy as np
from threading import Thread
from APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS import PRS
import matplotlib.pyplot as plt
import pandas as pd


# from APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS import PRS
def spherical_variogram_model(m, d):
    """Spherical model, m is [psill, range, nugget]"""
    psill = float(m[0])  # c1
    range_ = float(m[1])  # c2
    nugget = float(m[2])  # c0
    return np.piecewise(
        d,
        [d <= range_, d > range_],
        [
            lambda x: psill * ((3.0 * x) / (2.0 * range_) - (x ** 3.0) / (2.0 * range_ ** 3.0)) + nugget,
            psill + nugget,
        ],
    )


def a(m, d):
    c1 = float(m[0])  # c1
    c2 = float(m[1])  # c2
    c0 = float(m[2])  # c0
    return np.piecewise(
        d,
        [d <= c2, d > c2],
        [
            lambda x: c1 * ((3.0 * x) / (2.0 * c2) - (x ** 3.0) / (2.0 * c2 ** 3.0)) + c0,
            c1 + c0,
        ],
    )


def spherical(_d, _theta):
    m, n = _d.shape
    td = min(abs(_d) * np.tile(_theta, m).any(), [1])
    print(td)
    return list(map(lambda _x: 1 - (1.5 * _x / _theta - (_x ** 3.0) / (2.0 * _theta ** 3.0)), _d))


# d = np.array([1, 2, 3]).reshape(-1, 3)
# theta = np.array([2, 3, 4])
# spherical(d, theta)

# print(min([1, 3, 4], [1, 1, 1]))


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

# x_train = np.array([[3, 2, 5], [2, 3, 4], [4, 5, 6]])
# y_train = np.array([4, 5, 5])
# x_pre = np.array([[3, 4, 5]])
# p = PRS(m=1)
# p.calc_gram_matrix(x_train)
# print(p.gram_matrix)
# p.fit(y_train)
# p.predict(x_pre)

# x = np.arange(0, 10)
# print(x)
# xx = np.piecewise(x, [x < 4, x >= 6], [-1, 1])
# print(xx)
# print(spherical_variogram_model(np.array([3, 4, 5]), 6))
def Read_SData(path):
    list_different_angle = []
    file_content = open(path, 'rt')
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []
    list_8 = []
    list_angle = []
    i = 0
    for line in file_content:
        i += 1
        if i % 16 == 1:
            list_1.append(np.abs(float(line)))
        elif i % 16 == 2:
            list_angle.append(float(line))
        elif i % 16 == 3:
            list_2.append(float(line))
        elif i % 16 == 5:
            list_3.append(float(line))
        elif i % 16 == 7:
            list_4.append(float(line))
        elif i % 16 == 9:
            list_5.append(float(line))
        elif i % 16 == 11:
            list_6.append(float(line))
        elif i % 16 == 13:
            list_7.append(float(line))
        elif i % 16 == 15:
            list_8.append(float(line))
        else:
            continue
    file_content.close()
    return list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_angle


# path_test = r"D:\Alai\paper_Alai\【1】期刊论文\【1】Journal of Mechanical Design\起重机论文\v1.0\paper_result_truss\20200713_stress_data\\"
# load = "23_2"
# list_real_time_simulation_data = Read_SData(path_test + load + r".txt")
# pf = pd.DataFrame(list_real_time_simulation_data[8])
# pf.to_csv(r'C:\Users\laisir\Desktop\1.csv', header=False, index=False)
# plt.plot(range(len(list_real_time_simulation_data[0])), list_real_time_simulation_data[8])
# plt.show()

import os
from Demo.Telescopic_boom_2021.libs.element_data import ElementData

# # 读取并转换焊缝节点
# weld_joint_path = r"H:\Code\SANY_TB_DT\DT_Telescopic_Boom_v2.0\APP_models\pre_telescopic_boom_v1.0\Weld\\"
# all_files = os.listdir(weld_joint_path)
# list_weld_joint_threejs = []
# for _i, _file in enumerate(all_files):
#     weld_joint = pd.read_csv(weld_joint_path + _file)
#     _list_weld_joint_threejs = []
#     # print(weld_joint.values)
#     for _weld_joint in weld_joint.values:
#         _list_weld_joint_threejs.append(ele_index_threejs_dict[_weld_joint[0]])
#     list_weld_joint_threejs.append(_list_weld_joint_threejs)
import json

"""
因为json字符串中对象种类过多，load第一次解析出来的是str，再loads一次才能是字典对象
"""
path_prefix = r"H:\Code\SANY_TB_DT\DT_Telescopic_Boom_v2.0\APP_models\\"

path_switch = r'pre_telescopic_boom_v3.0\\'
path_read = path_prefix + path_switch
# prs_type = 'simple_m'
prs_type = 'full'

with open(path_read + path_switch[4:-7] + "_ele_coord_prs.json",
          "r") as f:
    dict_c_e = json.loads(json.load(f))

print(max(dict_c_e["elements_index"][0]))
print(max(dict_c_e["elements_index"][1]))
print(max(dict_c_e["elements_index"][2]))
print(max(dict_c_e["elements_index"][3]))
