from Demo.Telescopic_boom_2021.libs.element_data import ElementData
from APP_utils.Algorithm.Surrogate_Model.PRS.bp_complicated_PRS import PRS
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

stresses_prediction_list_jin = []
displacement_prediction_list_jin = []
stresses_prediction_list_hui = []
displacement_prediction_list_hui = []
for _i_list in range(4):
    displacement_prediction = pd.read_csv(path_read + 'Displacement_' + str(_i_list + 1) + '.csv')
    stress_prediction = pd.read_csv(path_read + 'Stress_' + str(_i_list + 1) + '.csv')
    np_array_displacement_prediction_jin = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                                      displacement_prediction.values[:, 0:432]))
    np_array_stress_prediction_jin = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                                stress_prediction.values[:, 0:432]))

    np_array_displacement_prediction_hui = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                                      displacement_prediction.values[:, 444:]))
    np_array_stress_prediction_hui = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                                stress_prediction.values[:, 444:]))

    displacement_prediction_temp_list_jin = []
    stresses_prediction_temp_list_jin = []
    for _i, _ in enumerate(np_array_displacement_prediction_jin):
        if np_array_displacement_prediction_jin[_i][0] in set_ele_surface_list[_i_list]:
            displacement_prediction_temp_list_jin.append(np_array_displacement_prediction_jin[_i][1:])
            stresses_prediction_temp_list_jin.append(np_array_stress_prediction_jin[_i][1:])
    displacement_prediction_list_jin.append(np.array(displacement_prediction_temp_list_jin))
    stresses_prediction_list_jin.append(np.array(stresses_prediction_temp_list_jin))

    displacement_prediction_temp_list_hui = []
    stresses_prediction_temp_list_hui = []
    for _i, _ in enumerate(np_array_displacement_prediction_hui):
        if np_array_displacement_prediction_hui[_i][0] in set_ele_surface_list[_i_list]:
            displacement_prediction_temp_list_hui.append(np_array_displacement_prediction_hui[_i][1:])
            stresses_prediction_temp_list_hui.append(np_array_stress_prediction_hui[_i][1:])
    displacement_prediction_list_hui.append(np.array(displacement_prediction_temp_list_hui))
    stresses_prediction_list_hui.append(np.array(stresses_prediction_temp_list_hui))

list_w_stress_jin = []
list_w_displacement_jin = []
m = 0
gram_matrix = None
prs_type = 'full'
for i_component, _ in enumerate(stresses_prediction_list_jin):
    list_w_stress_component = []
    list_w_displacement_component = []
    np_array_component_stresses = stresses_prediction_list_jin[i_component]
    np_array_component_displacement = displacement_prediction_list_jin[i_component]
    for i_node, _ in enumerate(np_array_component_stresses):
        prs_stress_node = PRS(m=3)
        prs_displacement_node = PRS(m=3)
        if i_node == 0:
            m = prs_stress_node.m
            gram_matrix = prs_stress_node.calc_gram_matrix(np_array_combination_train_jin)
        prs_stress_node.gram_matrix = gram_matrix
        prs_displacement_node.gram_matrix = gram_matrix
        w_stress = prs_stress_node.fit(
            np_array_component_stresses[i_node])
        w_displacement = prs_displacement_node.fit(
            np_array_component_displacement[i_node])
        list_w_stress_component.append(w_stress)
        list_w_displacement_component.append(w_displacement)
        print(
            "\r" + str(i_component + 1) + " (jin) component(s): " + str(i_node + 1) + "/" + str(
                np_array_component_stresses.shape[0]) +
            ' model(s) have been built', end="")
    list_w_stress_jin.append(list_w_stress_component)
    list_w_displacement_jin.append(list_w_displacement_component)

list_w_stress_hui = []
list_w_displacement_hui = []
for i_component, _ in enumerate(stresses_prediction_list_hui):
    list_w_stress_component = []
    list_w_displacement_component = []
    np_array_component_stresses = stresses_prediction_list_hui[i_component]
    np_array_component_displacement = displacement_prediction_list_hui[i_component]
    for i_node, _ in enumerate(np_array_component_stresses):
        prs_stress_node = PRS(m=3)
        prs_displacement_node = PRS(m=3)
        if i_node == 0:
            m = prs_stress_node.m
            gram_matrix = prs_stress_node.calc_gram_matrix(np_array_combination_train_hui)
        prs_stress_node.gram_matrix = gram_matrix
        prs_displacement_node.gram_matrix = gram_matrix
        w_stress = prs_stress_node.fit(
            np_array_component_stresses[i_node])
        w_displacement = prs_displacement_node.fit(
            np_array_component_displacement[i_node])
        list_w_stress_component.append(w_stress)
        list_w_displacement_component.append(w_displacement)
        print(
            "\r" + str(i_component + 1) + " (hui) component(s): " + str(i_node + 1) + "/" + str(
                np_array_component_stresses.shape[0]) +
            ' model(s) have been built', end="")
    list_w_stress_hui.append(list_w_stress_component)
    list_w_displacement_hui.append(list_w_displacement_component)
"""
按照每个节点进行预测
"""
dict_prs_model = {
    "stress_w_jin": list_w_stress_jin,
    "deformation_w_jin": list_w_displacement_jin,
    "stress_w_hui": list_w_stress_hui,
    "deformation_w_hui": list_w_displacement_hui,
    "x_train": np_array_combination_train.flatten().tolist(),
    "prs_type": prs_type,
    "m": m,
}
json_prs_model = json.dumps(dict_prs_model)
with open(
        path_prefix + r'pre_telescopic_boom_v3.0\\' + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_s_d_prs.json",
        "w") as f:
    json.dump(json_prs_model, f)
