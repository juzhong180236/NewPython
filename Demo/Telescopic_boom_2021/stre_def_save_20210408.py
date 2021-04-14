from Demo.Telescopic_boom_2021.libs.element_data import ElementData
from Demo.Ansys_Data_Utils_2021.Surrogate_Models.RBF import RBF
import json
import numpy as np

"""
2021.04.08 RBF通过坐标值预测应力和位移，该方法矩阵过大30000*30000，失败。
"""

path_prefix = r"C:\Users\asus\Desktop\Code\DT_Telescopic_Boom_v1.0\APP_models\\"
# path_switch = 'rbf_correct_model'
path_switch = r'pre_telescopic_boom\\'
# 读取路径(读pre)
path_four_read = path_prefix + path_switch

elements = open(path_four_read + r'elements\1_1.txt', 'rt')
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
# # 在Three.js中可用的索引数据
# ele_data_save = ele_data.surfaceEle_Real_Sequence_aerofoil(path_four_read + r'coordinates\1_1.txt')
print("Element data has been loaded！")

"""
以1_1的网格作为最终的网格排布形态，所有后续的网格训练出的模型用1_1作为输入进行预测
"""
coordinates_benchmark = open(path_four_read + r'coordinates\1_1.txt', 'rt')
stresses_benchmark = open(path_four_read + r'stresses\1_1.txt', 'rt')
displacement_benchmark = open(path_four_read + r'displacement\1_1.txt', 'rt')

coordinates_benchmark_str = coordinates_benchmark.read()
stresses_benchmark_str = stresses_benchmark.read()
displacement_benchmark_str = displacement_benchmark.read()

coordinates_benchmark_list = coordinates_benchmark_str.split("C")
stresses_benchmark_list = coordinates_benchmark_str.split("C")
displacement_benchmark_list = coordinates_benchmark_str.split("C")

cd_benchmark_result_list = []
stresses_benchmark_result_list = []
displacement_benchmark_result_list = []
# 命名为C_1到C_4的Component，共4个Components，即4次循环
for i_list, _ in enumerate(coordinates_benchmark_list):
    cd_benchmark_component_list = []
    stresses_benchmark_component_list = []
    displacement_benchmark_component_list = []

    cd_temp_list = coordinates_benchmark_list[i_list].strip().split("\n")
    stresses_temp_list = stresses_benchmark_list[i_list].strip().split("\n")
    displacement_temp_list = displacement_benchmark_list[i_list].strip().split("\n")
    # 每个Component中的坐标，应力，位移个数。根据Component的不同循环次数不同
    for i_list_child, _ in enumerate(cd_temp_list):
        cd_list_child = cd_temp_list[i_list_child].split()

        cd_index = int(cd_list_child[0])
        if cd_index in set_ele_surface_list[i_list]:
            cd_benchmark_component_list.append([float(cd_list_child[1]),
                                                float(cd_list_child[2]),
                                                float(cd_list_child[3])])

            stresses_list_child = stresses_temp_list[i_list_child].split()
            displacement_list_child = displacement_temp_list[i_list_child].split()
            stresses_benchmark_component_list.append(float(stresses_list_child[1]))
            displacement_benchmark_component_list.append(float(stresses_list_child[1]))
    cd_benchmark_result_list.append(cd_benchmark_component_list)
    stresses_benchmark_result_list.append(stresses_benchmark_component_list)
    displacement_benchmark_result_list.append(displacement_benchmark_component_list)
np_array_cd_train = np.array(cd_benchmark_result_list)  # 以下所建立代理模型中预测的输入
coordinates_benchmark.close()

print("The data in the file 1_1 has been loaded！")

"""
第二次预测的输入
"""
degreeArr = [0, 30, 50, 70]
distanceArr = [100, 1200, 2400, 3600]
combine = []
for i_degree, _ in enumerate(degreeArr):
    for i_distance, _ in enumerate(distanceArr):
        combine.append((degreeArr[i_degree], distanceArr[i_distance]))
np_array_combination_train = np.array(combine)

print("The independent variables of the train set has been created！")

"""
1_2到1_16的网格作为训练集的输入，应力/位移作为输出建立模型
"""
rbf_type = "mq"
stresses_prediction_list = [stresses_benchmark_result_list]
displacement_prediction_list = [displacement_benchmark_result_list]

rbf_list = []
for i_file in range(1, 16):  # 2_1到16_1坐标，应力，位移文件。共15个文件15次循环
    coordinates = open(path_four_read + r'coordinates\\' + str(i_file + 1) + '_1.txt', 'rt')
    stresses = open(path_four_read + r'stresses\\' + str(i_file + 1) + '_1.txt', 'rt')
    displacement = open(path_four_read + r'displacement\\' + str(i_file + 1) + '_1.txt', 'rt')

    coordinates_str = coordinates.read()
    stresses_str = stresses.read()
    displacement_str = displacement.read()

    coordinates_list = coordinates_str.split("C")
    stresses_list = coordinates_str.split("C")
    displacement_list = coordinates_str.split("C")

    stresses_prediction_child_list = []
    displacement_prediction_child_list = []
    # 命名为C_1到C_4的Component，共4个Components，即4次循环
    for i_list, _ in enumerate(coordinates_list):

        cd_component_list = []
        stresses_component_list = []
        displacement_component_list = []

        cd_temp_list = coordinates_list[i_list].strip().split("\n")
        stresses_temp_list = stresses_list[i_list].strip().split("\n")
        displacement_temp_list = displacement_list[i_list].strip().split("\n")
        # 每个Component中的坐标，应力，位移个数。根据Component的不同循环次数不同
        for i_list_child, _ in enumerate(cd_temp_list):
            cd_list_child = cd_temp_list[i_list_child].split()
            cd_index = int(cd_list_child[0])
            if cd_index in set_ele_surface_list[i_list]:
                cd_component_list.append([float(cd_list_child[1]),
                                          float(cd_list_child[2]),
                                          float(cd_list_child[3])])
                stresses_list_child = stresses_temp_list[i_list_child].split()
                displacement_list_child = displacement_temp_list[i_list_child].split()
                stresses_component_list.append(float(stresses_list_child[1]))
                displacement_component_list.append(float(stresses_list_child[1]))
        print("The big model is building...")
        # 每个Component建立一个代理模型
        rbf_stress = RBF(rbf_type)
        rbf_displacement = RBF(rbf_type)
        np_array_cd_component = np.array(cd_component_list)
        rbf_stress.fit(np_array_cd_component, np.array(stresses_component_list))
        print(1)
        rbf_displacement.fit(np_array_cd_component, np.array(displacement_component_list))
        print(2)

        # 每个Component预测得到的应力和位移数据存放到list中
        stresses_prediction_child_list.append(list(rbf_stress.predict(np_array_cd_train[i_list])))
        displacement_prediction_child_list.append(list(rbf_displacement.predict(np_array_cd_train[i_list])))
        print("\r" + str(i_file) + " stage: " + str(i_list) + ' model(s) have been built', end="")

    coordinates.close()
    stresses_prediction_list.append(stresses_prediction_child_list)
    displacement_prediction_list.append(displacement_prediction_child_list)
    print("\rThe first training program is currently complete：" + str(round(i_file / 15 * 10000) / 100) + '%', end="")

np_array_stresses_prediction = np.array(stresses_prediction_list).T
np_array_displacement_prediction = np.array(displacement_prediction_list).T
print(np_array_stresses_prediction.shape)
# 命名为C_1到C_4的Component，分为16步应力和位移，4*16，共4个Components，即4次循环
list_w_stress = []
list_w_displacement = []
stds = None
for i_list, _ in enumerate(np_array_stresses_prediction):
    list_w_stress_component = []
    list_w_displacement_component = []
    np_array_stresses_component = np_array_stresses_prediction[i_list].T
    np_array_displacement_component = np_array_displacement_prediction[i_list].T
    for i_node, _ in enumerate(np_array_stresses_component):
        rbf_stress_node = RBF(rbf_type)
        rbf_displacement_node = RBF(rbf_type)
        w_stress = rbf_stress_node.fit(np_array_combination_train, np_array_stresses_component[i_node])
        w_displacement = rbf_displacement_node.fit(np_array_combination_train, np_array_displacement_component[i_node])
        if i_node == 0:
            stds = rbf_stress_node.std
        list_w_stress_component.append(w_stress)
        list_w_displacement_component.append(w_displacement)
    list_w_stress.append(list_w_stress_component)
    list_w_displacement.append(list_w_displacement_component)

"""
按照每个节点进行预测
"""

dict_rbf_model = {

    "stress_w": list_w_stress,
    # "stress_step": s_step,
    # "stress_min": s_min,

    "deformation_w": list_w_displacement,
    # "deformation_step": d_step,
    # "deformation_min": d_min,

    "stds": stds,
    "x_train": np_array_combination_train.flatten().tolist(),
    "rbf_type": rbf_type,
}

json_rbf_model = json.dumps(dict_rbf_model)
with open("C:/Users/asus/Desktop/" + path_switch[4:-2] + "_rbf_s_d.json", "w") as f:
    json.dump(json_rbf_model, f)
