from Demo.Telescopic_boom_2021.libs.element_data import ElementData
from APP_utils.Algorithm.Surrogate_Model.PRS.simple_multiple_PRS import PRS
import Demo.Telescopic_boom_2021.coordinate_transform.coordinate_transform as ct
import json
import numpy as np
from scipy.interpolate import griddata
import pandas as pd

"""
因为ansys中的文件顺序（也就是工况顺序）是乱序排列，所以要使用filename_sort将文件排列好后进行训练
"""
path_prefix = r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"
path_switch = r'pre_telescopic_boom_v2.0\\'

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
# list_ele_surface_list = ele_data.surfaceEle_Sequence_aerofoil()
set_ele_surface_list = ele_data.set_SurfaceEle_aerofoil()
# 在Three.js中可用的索引数据
ele_data_save = ele_data.surfaceEle_Real_Sequence_aerofoil(
    path_read + r'coordinates.txt')

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
print("The independent variables of the train set has been created！")
print("The working condition-based model is building...")
stresses_prediction_list = []
displacement_prediction_list = []
coordinates_list = []
for _i_list in range(4):
    displacement_prediction = pd.read_csv(path_read + 'Displacement_' + str(_i_list + 1) + '.csv')
    stress_prediction = pd.read_csv(path_read + 'Stress_' + str(_i_list + 1) + '.csv')
    np_array_displacement_prediction = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                                  displacement_prediction.values[:, 0:432],
                                                  displacement_prediction.values[:, 444:]))

    np_array_stress_prediction = np.hstack((np.array([cd_index_list[_i_list]]).reshape(-1, 1),
                                            stress_prediction.values[:, 0:432],
                                            stress_prediction.values[:, 444:]))
    displacement_prediction_temp_list = []
    stresses_prediction_temp_list = []
    for _i, _ in enumerate(np_array_stress_prediction):
        if np_array_stress_prediction[_i][0] in set_ele_surface_list[_i_list]:
            displacement_prediction_temp_list.append(np_array_displacement_prediction[_i][1:])
            stresses_prediction_temp_list.append(np_array_stress_prediction[_i][1:])
    displacement_prediction_list.append(np.array(displacement_prediction_temp_list))
    stresses_prediction_list.append(np.array(stresses_prediction_temp_list))

list_w_stress = []
list_w_displacement = []
m = 0
gram_matrix = None
prs_type = 'simple_m'
for i_component, _ in enumerate(stresses_prediction_list):
    list_w_stress_component = []
    list_w_displacement_component = []
    np_array_component_stresses = stresses_prediction_list[i_component]
    np_array_component_displacement = displacement_prediction_list[i_component]
    for i_node, _ in enumerate(np_array_component_stresses):
        prs_stress_node = PRS(m=3)
        prs_displacement_node = PRS(m=3)
        if i_node == 0:
            m = prs_stress_node.m
            gram_matrix = prs_stress_node.calc_gram_matrix(np_array_combination_train)
        prs_stress_node.gram_matrix = gram_matrix
        prs_displacement_node.gram_matrix = gram_matrix
        w_stress = prs_stress_node.fit(
            np_array_component_stresses[i_node])
        w_displacement = prs_displacement_node.fit(
            np_array_component_displacement[i_node])
        list_w_stress_component.append(w_stress)
        list_w_displacement_component.append(w_displacement)
        print(
            "\r" + str(i_component + 1) + " component(s): " + str(i_node + 1) + "/" + str(
                np_array_component_stresses.shape[0]) +
            ' model(s) have been built', end="")
    list_w_stress.append(list_w_stress_component)
    list_w_displacement.append(list_w_displacement_component)
"""
按照每个节点进行预测
"""
dict_prs_model = {
    "stress_w": list_w_stress,
    "deformation_w": list_w_displacement,
    "x_train": np_array_combination_train.flatten().tolist(),
    "prs_type": prs_type,
    "m": m,
}
json_prs_model = json.dumps(dict_prs_model)
with open(r"H:\Code\DT_Telescopic_Boom_v2.0\APP_models\\"
          + r"prs\\" + prs_type + r"\\" + path_switch[4:-7] + "_s_d_prs.json", "w") as f:
    json.dump(json_prs_model, f)
