from Demo.Telescopic_boom_2021.element_data import ElementData
from Demo.Telescopic_boom_2021.coordinate_data import CoordinateData
import json

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
list_ele_surface_list = ele_data.surfaceEle_Sequence_aerofoil()
set_ele_surface_list = ele_data.set_SurfaceEle_aerofoil()
# 在Three.js中可用的索引数据
ele_data_save = ele_data.surfaceEle_Real_Sequence_aerofoil(path_four_read + r'coordinates\1_1.txt')

coordinates = open(path_four_read + r'coordinates\1_1.txt', 'rt')
coordinates_str = coordinates.read()
coordinates_list = coordinates_str.split("C")
cd_result_list = []
for i_cd_list in range(len(coordinates_list)):
    cd_component_list = []
    temp_list = coordinates_list[i_cd_list].strip().split("\n")
    for temp_list_child in temp_list:
        _list = temp_list_child.split()
        cd_index = int(_list[0])
        if cd_index in set_ele_surface_list[i_cd_list]:
            cd_x = float(_list[1])
            cd_y = float(_list[2])
            cd_z = float(_list[3])
            cd_component_list.extend([cd_x, cd_y, cd_z])
    cd_result_list.append(cd_component_list)
coordinates.close()
dict_rbf_model = {
    "coordinates": cd_result_list,
    "elements_index": ele_data_save,

    # "stress_w": list_w_stress,
    # "stress_step": s_step,
    # "stress_min": s_min,
    #
    # "deformation_w": list_w_dSum,
    # "deformation_step": d_step,
    # "deformation_min": d_min,
    #
    # "y_w": list_w_y,
    # "z_w": list_w_z,
    #
    # "stds": stds,
    # "x_train": x_train,
    # "rbf_type": rbf_type,
}

json_rbf_model = json.dumps(dict_rbf_model)
with open("C:/Users/asus/Desktop/" + path_switch[4:-2] + "_rbf.json", "w") as f:
    json.dump(json_rbf_model, f)
