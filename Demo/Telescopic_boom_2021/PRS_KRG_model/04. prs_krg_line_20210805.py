from Demo.Telescopic_boom_2021.libs.element_data import ElementData
from APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS import PRS
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.Kriging import Kriging
import Demo.Telescopic_boom_2021.coordinate_transform.coordinate_transform as ct
import json
import numpy as np
from scipy.interpolate import griddata
import pandas as pd

"""
3.3度的伸缩臂，应力和变形数据没有索引
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"
path_switch = r'pre_telescopic_boom_v1.0\\'

# 读取路径(读pre)
path_read = path_prefix + path_switch
"""
预测的输入
"""
index_max = pd.read_csv(path_read + 'Index_max.csv')
# print(index_max)
elements = open(path_read + r'elements.txt', 'rt')
elements_str = elements.read()
elements_list = elements_str.split("C")
ele_result_list = []
for ele_str in elements_list:
    ele_component_list = []
    temp_list = ele_str.strip().split("\n")
    for temp_list_child in temp_list:
        _list = temp_list_child.split()
        ele_number = int(_list[0])
        node_1 = int(_list[1])
        node_2 = int(_list[2])
        node_3 = int(_list[3])
        node_4 = int(_list[4])
        node_5 = int(_list[5])
        node_6 = int(_list[6])
        node_7 = int(_list[7])
        node_8 = int(_list[8])
        ele_component_list.append(
            [ele_number, node_1, node_2, node_3, node_4,
             node_5, node_6, node_7, node_8])
    ele_result_list.append(ele_component_list)
elements.close()

ele_data = ElementData(geometry_type=['3D4_P'], data_list=ele_result_list)
set_ele_surface_list = ele_data.set_SurfaceEle_aerofoil()

coordinates = open(path_read + r'coordinates.txt', 'rt')
coordinates_str = coordinates.read()
coordinates_list = coordinates_str.split("C")
cd_result_list = []
cd_result_list_negative = []
cd_index_list = []
cd_z_max_list = []
# 命名为C_1到C_4的Component，共4个Components，即4次循环
for i_cd_list, _ in enumerate(coordinates_list):
    cd_component_list = []
    cd_component_list_negative = []
    cd_component_list_index = []
    temp_list = coordinates_list[i_cd_list].strip().split("\n")
    # 每个Component中的坐标，应力，位移个数。根据Component的不同循环次数不同
    for i_list_child, _ in enumerate(temp_list):
        _list = temp_list[i_list_child].split()
        cd_index = int(_list[0])
        cd_component_list_index.append(cd_index)
        if i_cd_list == 0:
            if cd_index in index_max.values:
                cd_z_max_list.append(float(_list[3]))
        if cd_index in set_ele_surface_list[i_cd_list]:
            cd_x = float(_list[1])
            cd_y = float(_list[2])
            cd_z = float(_list[3])
            cd_component_list.extend([cd_x, cd_y, cd_z])
            cd_component_list_negative.extend([-cd_x, cd_y, cd_z])
    cd_result_list.append(cd_component_list)
    cd_result_list_negative.append(cd_component_list_negative)
    cd_index_list.append(cd_component_list_index)
coordinates.close()

"""
预测的输入
"""
combine = pd.read_csv(path_read + 'X_train1.txt', sep='\t', names=['载荷', '角度', '位移', '油压'])
np_array_combination_train = combine.values[:, 0:3]
np_array_combination_train_jin = np_array_combination_train[0:432, :]
np_array_combination_train_hui = np_array_combination_train[432:, :]

print("The independent variables of the train set has been created！")
print("The working condition-based model is building...")

stress_jin_max = pd.read_csv(path_read + 'Stress_jin_max.csv')
list_w_stress_jin_prs = []
list_w_stress_jin_krg = []
m = 0
gram_matrix = None
prs_type = 'full'
for i_node, _ in enumerate(stress_jin_max.values):
    prs_stress_node = PRS(m=3)
    krg_stress_node = Kriging()
    if i_node == 0:
        m = prs_stress_node.m
        gram_matrix = prs_stress_node.calc_gram_matrix(np_array_combination_train_jin)
    prs_stress_node.gram_matrix = gram_matrix
    w_stress_prs = prs_stress_node.fit(stress_jin_max.values[i_node])
    w_stress_krg = krg_stress_node.train(np_array_combination_train_jin, stress_jin_max.values[i_node])
    list_w_stress_jin_prs.append(w_stress_prs)
    list_w_stress_jin_krg.append(w_stress_krg)
    print("\r" + str(i_node + 1) + "/" + str(stress_jin_max.values.shape[0]) +
          ' model(s) have been built', end="")

stress_hui_max = pd.read_csv(path_read + 'Stress_hui_max.csv')
list_w_stress_hui_prs = []
list_w_stress_hui_krg = []
for i_node, _ in enumerate(stress_hui_max.values):
    prs_stress_node = PRS(m=3)
    krg_stress_node = Kriging()
    if i_node == 0:
        m = prs_stress_node.m
        gram_matrix = prs_stress_node.calc_gram_matrix(np_array_combination_train_hui)
    prs_stress_node.gram_matrix = gram_matrix
    w_stress_prs = prs_stress_node.fit(stress_hui_max.values[i_node])
    w_stress_krg = krg_stress_node.train(np_array_combination_train_jin, stress_jin_max[i_node])
    list_w_stress_hui_prs.append(w_stress_prs)
    list_w_stress_hui_krg.append(w_stress_krg)
    print("\r" + str(i_node + 1) + "/" + str(stress_hui_max.values.shape[0]) +
          ' model(s) have been built', end="")
"""
按照每个节点进行预测
"""
dict_prs_model = {
    "stress_w_jin_prs": list_w_stress_jin_prs,
    "stress_w_jin_krg": list_w_stress_jin_krg,
    "stress_w_hui_prs": list_w_stress_hui_prs,
    "stress_w_hui_krg": list_w_stress_hui_krg,
    "y_max_jin": stress_jin_max.values.tolist(),
    "y_max_hui": stress_hui_max.values.tolist(),
    "line_z_coordinates": cd_z_max_list,
}

json_prs_model = json.dumps(dict_prs_model)
with open(
        path_prefix + r'pre_telescopic_boom_v3.0\\' + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_s_d_prs.json",
        "w") as f:
    json.dump(json_prs_model, f)
